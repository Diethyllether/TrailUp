from datetime import datetime
from functools import wraps

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from models.trilha_model import Trilha
from models.usuario_model import Usuario
from services.casos_uso import CadastrarUsuarioService, LoginUsuarioService
from services.checkpoint_service import CheckpointService
from services.evento_service import EventoService
from services.favorito_service import FavoritoService
from services.trilha_service import TrilhaService

web_bp = Blueprint("web_bp", __name__)


class WebController:
    """Controller das páginas HTML do TrailUp.

    O site usa Jinja2 para renderização inicial e reutiliza a mesma camada de
    Services/Models da API, evitando duplicar regra de negócio no frontend.
    """

    def __init__(self):
        self.login_service = LoginUsuarioService()
        self.cadastrar_service = CadastrarUsuarioService()
        self.trilha_service = TrilhaService()
        self.checkpoint_service = CheckpointService()
        self.evento_service = EventoService()
        self.favorito_service = FavoritoService()

    @staticmethod
    def _usuario_logado():
        id_usuario = session.get("id_usuario")
        return Usuario.buscar_por_id(id_usuario) if id_usuario else None

    @staticmethod
    def _login_obrigatorio(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.get("id_usuario"):
                flash("Entre na sua conta para continuar.", "info")
                return redirect(url_for("web_bp.login", proxima=request.path))
            return func(*args, **kwargs)

        return wrapper

    def _contexto_base(self):
        return {
            "usuario_logado": self._usuario_logado(),
            "google_maps_api_key": current_app.config.get("GOOGLE_MAPS_API_KEY", ""),
        }

    def inicio(self):
        busca = (request.args.get("busca") or "").strip()
        dificuldade = (request.args.get("dificuldade") or "").strip() or None
        trilhas = self.trilha_service.buscar(busca=busca or None, dificuldade=dificuldade)
        eventos = self.evento_service.listar_todos()

        favoritos_ids = set()
        usuario = self._usuario_logado()
        if usuario:
            favoritos_ids = {
                favorito.idTrilha
                for favorito in self.favorito_service.listar_por_usuario(usuario.idUsuario)
            }

        return render_template(
            "home.html",
            trilhas=trilhas,
            eventos=eventos[:6],
            favoritos_ids=favoritos_ids,
            busca=busca,
            dificuldade=dificuldade or "",
            **self._contexto_base(),
        )

    def login(self):
        if request.method == "GET":
            if session.get("id_usuario"):
                return redirect(url_for("web_bp.inicio"))
            return render_template("login.html", **self._contexto_base())

        try:
            _, usuario = self.login_service.executar(
                request.form.get("email", "").strip(),
                request.form.get("senha", ""),
            )
            session.clear()
            session["id_usuario"] = usuario.idUsuario
            flash(f"Bem-vindo, {usuario.nome}!", "success")
            destino = request.args.get("proxima")
            if destino and destino.startswith("/"):
                return redirect(destino)
            return redirect(url_for("web_bp.inicio"))
        except ValueError as erro:
            flash(str(erro), "danger")
            return render_template("login.html", email=request.form.get("email", ""), **self._contexto_base()), 401

    def cadastro(self):
        if request.method == "GET":
            return render_template("register.html", **self._contexto_base())

        try:
            usuario = self.cadastrar_service.executar(
                {
                    "nome": request.form.get("nome", "").strip(),
                    "email": request.form.get("email", "").strip(),
                    "senha": request.form.get("senha", ""),
                }
            )
            session.clear()
            session["id_usuario"] = usuario.idUsuario
            flash("Conta criada com sucesso.", "success")
            return redirect(url_for("web_bp.inicio"))
        except ValueError as erro:
            flash(str(erro), "danger")
            return render_template("register.html", **self._contexto_base()), 400

    def logout(self):
        session.clear()
        flash("Sessão encerrada.", "info")
        return redirect(url_for("web_bp.inicio"))

    def trilha(self, id_trilha):
        try:
            trilha = self.trilha_service.buscar_por_id(id_trilha)
        except ValueError:
            return render_template("404.html", **self._contexto_base()), 404

        checkpoints = [
            cp.to_dict()
            for cp in self.checkpoint_service.listar_por_trilha(id_trilha)
            if cp.latitude is not None
            and cp.longitude is not None
            and not (cp.latitude == 0 and cp.longitude == 0)
        ]
        eventos = [self.evento_service.to_dict_completo(e) for e in self.evento_service.listar_por_trilha(id_trilha)]

        favorito = False
        usuario = self._usuario_logado()
        if usuario:
            favorito = any(
                item.idTrilha == id_trilha
                for item in self.favorito_service.listar_por_usuario(usuario.idUsuario)
            )

        return render_template(
            "trail_detail.html",
            trilha=trilha,
            checkpoints=checkpoints,
            eventos=eventos,
            favorito=favorito,
            **self._contexto_base(),
        )

    @_login_obrigatorio
    def alternar_favorito(self, id_trilha):
        id_usuario = session["id_usuario"]
        favoritos = self.favorito_service.listar_por_usuario(id_usuario)
        if any(item.idTrilha == id_trilha for item in favoritos):
            self.favorito_service.remover(id_usuario, id_trilha)
            flash("Trilha removida dos favoritos.", "info")
        else:
            self.favorito_service.adicionar(id_usuario, id_trilha)
            flash("Trilha adicionada aos favoritos.", "success")
        return redirect(request.referrer or url_for("web_bp.inicio"))

    @_login_obrigatorio
    def favoritos(self):
        favoritos = self.favorito_service.listar_por_usuario(session["id_usuario"])
        trilhas = [Trilha.buscar_por_id(item.idTrilha) for item in favoritos]
        trilhas = [trilha for trilha in trilhas if trilha]
        return render_template("favorites.html", trilhas=trilhas, **self._contexto_base())

    def eventos(self):
        eventos = [self.evento_service.to_dict_completo(e) for e in self.evento_service.listar_todos()]
        trilhas = self.trilha_service.listar_todos()
        return render_template("events.html", eventos=eventos, trilhas=trilhas, **self._contexto_base())

    @_login_obrigatorio
    def criar_evento(self):
        try:
            data_texto = request.form.get("data", "").strip()
            horario_texto = request.form.get("horario", "").strip()
            data_evento = datetime.strptime(data_texto, "%Y-%m-%d").date() if data_texto else None
            horario_saida = None
            if data_texto and horario_texto:
                horario_saida = datetime.strptime(f"{data_texto} {horario_texto}", "%Y-%m-%d %H:%M")

            id_trilha = int(request.form["idTrilha"])
            dados = {
                "titulo": request.form.get("titulo", "").strip(),
                "descricao": request.form.get("descricao", "").strip() or None,
                "data": data_evento,
                "horarioSaida": horario_saida,
                "imediata": request.form.get("imediata") == "on",
                "vagas": int(request.form["vagas"]) if request.form.get("vagas") else None,
                "tipo": request.form.get("tipo", "GRUPO"),
                "trilhas": [id_trilha],
            }
            self.evento_service.criar(session["id_usuario"], dados)
            flash("Expedição criada com sucesso.", "success")
        except (ValueError, KeyError) as erro:
            flash(str(erro), "danger")
        return redirect(url_for("web_bp.eventos"))

    @_login_obrigatorio
    def participar_evento(self, id_evento):
        try:
            self.evento_service.entrar(id_evento, session["id_usuario"])
            flash("Você entrou na expedição.", "success")
        except ValueError as erro:
            flash(str(erro), "danger")
        return redirect(request.referrer or url_for("web_bp.eventos"))

    @_login_obrigatorio
    def perfil(self):
        usuario = self._usuario_logado()
        favoritos = self.favorito_service.listar_por_usuario(usuario.idUsuario)
        return render_template(
            "profile.html",
            usuario=usuario,
            total_favoritos=len(favoritos),
            **self._contexto_base(),
        )


controller = WebController()
web_bp.add_url_rule("/", "inicio", controller.inicio, methods=["GET"])
web_bp.add_url_rule("/login", "login", controller.login, methods=["GET", "POST"])
web_bp.add_url_rule("/cadastro", "cadastro", controller.cadastro, methods=["GET", "POST"])
web_bp.add_url_rule("/logout", "logout", controller.logout, methods=["POST"])
web_bp.add_url_rule("/trilhas/<int:id_trilha>", "trilha", controller.trilha, methods=["GET"])
web_bp.add_url_rule("/trilhas/<int:id_trilha>/favorito", "alternar_favorito", controller.alternar_favorito, methods=["POST"])
web_bp.add_url_rule("/favoritos", "favoritos", controller.favoritos, methods=["GET"])
web_bp.add_url_rule("/eventos", "eventos", controller.eventos, methods=["GET"])
web_bp.add_url_rule("/eventos", "criar_evento", controller.criar_evento, methods=["POST"])
web_bp.add_url_rule("/eventos/<int:id_evento>/participar", "participar_evento", controller.participar_evento, methods=["POST"])
web_bp.add_url_rule("/perfil", "perfil", controller.perfil, methods=["GET"])
