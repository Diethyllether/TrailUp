"""Rotas JSON temporárias; a Fase 4 as extrai para Blueprints por recurso."""

from flask import Blueprint, jsonify, request, session

from services.avaliacao.atualizar_avaliacao_service import AtualizarAvaliacaoService
from services.avaliacao.excluir_avaliacao_service import ExcluirAvaliacaoService
from services.avaliacao.publicar_avaliacao_service import PublicarAvaliacaoService
from services.checklist.consultar_checklist_service import ConsultarChecklistService
from services.checklist.marcar_item_checklist_service import MarcarItemChecklistService
from services.denuncia.reportar_problema_service import ReportarProblemaService
from services.evento.atualizar_evento_service import AtualizarEventoService
from services.evento.cancelar_evento_service import CancelarEventoService
from services.evento.comentar_evento_service import ComentarEventoService
from services.evento.criar_evento_service import CriarEventoService
from services.evento.listar_eventos_ativos_service import ListarEventosAtivosService
from services.evento.participar_evento_service import ParticiparEventoService
from services.evento.sair_evento_service import SairEventoService
from services.favorito.adicionar_favorito_service import AdicionarFavoritoService
from services.favorito.listar_favoritos_service import ListarFavoritosService
from services.favorito.remover_favorito_service import RemoverFavoritoService
from services.historico.consultar_historico_service import ConsultarHistoricoService
from services.historico.registrar_trilha_concluida_service import RegistrarTrilhaConcluidaService
from services.trilha.buscar_trilhas_service import BuscarTrilhasService
from services.trilha.detalhar_trilha_service import DetalharTrilhaService
from services.usuario.atualizar_perfil_service import AtualizarPerfilService
from services.usuario.autenticar_usuario_service import AutenticarUsuarioService
from services.usuario.cadastrar_usuario_service import CadastrarUsuarioService
from services.usuario.consultar_sessao_service import ConsultarSessaoService
from services.usuario.redefinir_senha_service import RedefinirSenhaService
from services.usuario.solicitar_recuperacao_senha_service import SolicitarRecuperacaoSenhaService
from utils.decorators import login_obrigatorio


api_bp = Blueprint("api", __name__)


@api_bp.get("/session")
def get_session():
    usuario = ConsultarSessaoService().executar(session.get("id_usuario"))
    return jsonify(user=usuario)


@api_bp.post("/auth/login")
def login():
    dados = request.get_json(silent=True) or {}
    usuario = AutenticarUsuarioService().executar(dados.get("email"), dados.get("senha"))
    session.clear()
    session["id_usuario"] = usuario["idUsuario"]
    return jsonify(user=usuario)


@api_bp.post("/auth/register")
def register():
    dados = request.get_json(silent=True) or {}
    usuario = CadastrarUsuarioService().executar(dados)
    session.clear()
    session["id_usuario"] = usuario["idUsuario"]
    return jsonify(user=usuario), 201


@api_bp.post("/auth/logout")
def logout():
    session.clear()
    return jsonify(message="Sessão encerrada")


@api_bp.get("/trails")
def list_trails():
    itens = BuscarTrilhasService().executar(
        termo=request.args.get("q"),
        dificuldade=request.args.get("difficulty"),
        distancia_max=request.args.get("maxDistance"),
        duracao_max=request.args.get("maxDuration"),
        nota_min=request.args.get("minRating"),
        ordem=request.args.get("sort"),
        latitude=request.args.get("lat"),
        longitude=request.args.get("lon"),
        id_usuario=session.get("id_usuario"),
    )
    return jsonify(items=itens)


@api_bp.get("/trails/<int:trail_id>")
def trail_detail(trail_id):
    dados = DetalharTrilhaService().executar(trail_id, session.get("id_usuario"))
    return jsonify(**dados)


@api_bp.route("/trails/<int:trail_id>/favorite", methods=["POST", "DELETE"])
@login_obrigatorio
def favorite_trail(trail_id):
    usuario = session["id_usuario"]
    if request.method == "POST":
        AdicionarFavoritoService().executar(usuario, trail_id)
        return jsonify(favorite=True)
    RemoverFavoritoService().executar(usuario, trail_id)
    return jsonify(favorite=False)


@api_bp.get("/favorites")
@login_obrigatorio
def list_favorites():
    return jsonify(items=ListarFavoritosService().executar(session["id_usuario"]))


@api_bp.get("/events")
def list_events():
    dados = ListarEventosAtivosService().executar(session.get("id_usuario"))
    return jsonify(**dados)


@api_bp.post("/events")
@login_obrigatorio
def create_event():
    dados = request.get_json(silent=True) or {}
    evento = CriarEventoService().executar(session["id_usuario"], dados)
    return jsonify(event=evento), 201


@api_bp.post("/events/<int:event_id>/participation")
@login_obrigatorio
def join_event(event_id):
    dados = ParticiparEventoService().executar(event_id, session["id_usuario"])
    return jsonify(**dados)


@api_bp.delete("/events/<int:event_id>/participation")
@login_obrigatorio
def leave_event(event_id):
    dados = SairEventoService().executar(event_id, session["id_usuario"])
    return jsonify(**dados)


@api_bp.post("/trails/<int:trail_id>/reviews")
@login_obrigatorio
def create_review(trail_id):
    dados = request.get_json(silent=True) or {}
    PublicarAvaliacaoService().executar(session["id_usuario"], trail_id, dados)
    return jsonify(message="Avaliação publicada"), 201


@api_bp.route("/reviews/<int:review_id>", methods=["PUT", "DELETE"])
@login_obrigatorio
def update_review(review_id):
    if request.method == "DELETE":
        ExcluirAvaliacaoService().executar(review_id, session["id_usuario"])
        return "", 204
    dados = request.get_json(silent=True) or {}
    avaliacao = AtualizarAvaliacaoService().executar(
        review_id, session["id_usuario"], dados
    )
    return jsonify(review=avaliacao)


@api_bp.get("/history")
@login_obrigatorio
def list_history():
    itens = ConsultarHistoricoService().executar(session["id_usuario"])
    return jsonify(items=itens)


@api_bp.post("/history")
@login_obrigatorio
def create_history():
    dados = request.get_json(silent=True) or {}
    item = RegistrarTrilhaConcluidaService().executar(session["id_usuario"], dados)
    return jsonify(item=item), 201


@api_bp.patch("/profile")
@login_obrigatorio
def update_profile():
    dados = request.get_json(silent=True) or {}
    usuario = AtualizarPerfilService().executar(session["id_usuario"], dados)
    return jsonify(user=usuario)


@api_bp.post("/events/<int:event_id>/comments")
@login_obrigatorio
def comment_event(event_id):
    dados = request.get_json(silent=True) or {}
    comentario = ComentarEventoService().executar(
        event_id, session["id_usuario"], dados.get("texto")
    )
    return jsonify(comment=comentario), 201


@api_bp.route("/events/<int:event_id>", methods=["PUT", "DELETE"])
@login_obrigatorio
def manage_event(event_id):
    if request.method == "DELETE":
        CancelarEventoService().executar(event_id, session["id_usuario"])
        return "", 204
    dados = request.get_json(silent=True) or {}
    evento = AtualizarEventoService().executar(event_id, session["id_usuario"], dados)
    return jsonify(event=evento)


@api_bp.post("/reports")
@login_obrigatorio
def create_report():
    dados = request.get_json(silent=True) or {}
    denuncia = ReportarProblemaService().executar(session["id_usuario"], dados)
    return jsonify(report=denuncia), 201


@api_bp.get("/trails/<int:trail_id>/checklist-state")
@login_obrigatorio
def consultar_checklist(trail_id):
    dados = ConsultarChecklistService().executar(session["id_usuario"], trail_id)
    return jsonify(**dados)


@api_bp.patch("/checklist/<int:item_id>")
@login_obrigatorio
def marcar_item_checklist(item_id):
    dados = request.get_json(silent=True) or {}
    item = MarcarItemChecklistService().executar(
        session["id_usuario"], item_id, dados.get("marcado")
    )
    return jsonify(item=item)


@api_bp.post("/auth/password-reset")
def request_password_reset():
    email = ((request.get_json(silent=True) or {}).get("email") or "").strip()
    SolicitarRecuperacaoSenhaService().executar(email)
    return jsonify(message="Se o e-mail estiver cadastrado, enviaremos um link de recuperação.")


@api_bp.post("/auth/password-reset/confirm")
def confirm_password_reset():
    dados = request.get_json(silent=True) or {}
    RedefinirSenhaService().executar(dados.get("token"), dados.get("senha", ""))
    return jsonify(message="Senha redefinida com sucesso.")
