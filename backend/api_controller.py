from datetime import date, datetime
from email.message import EmailMessage
from functools import wraps
import os
import smtplib

from flask import Blueprint, jsonify, request, session
from sqlalchemy.exc import SQLAlchemyError

from config import Config
from extensions import db
from services.avaliacao_service import AvaliacaoService
from services.checklist_service import ChecklistService
from services.denuncia_service import DenunciaService
from services.checkpoint_service import CheckpointService
from services.evento_service import EventoService
from services.favorito_service import FavoritoService
from services.historico_service import HistoricoService
from services.trilha_service import TrilhaService
from services.usuario_service import UsuarioService

api_bp = Blueprint("api", __name__)
users, trails, events = UsuarioService(), TrilhaService(), EventoService()
favorites, ratings = FavoritoService(), AvaliacaoService()
checkpoints, checklists, history = CheckpointService(), ChecklistService(), HistoricoService()
reports = DenunciaService()


def fail(message, status=400):
    return jsonify(error=str(message)), status


def authenticated(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("id_usuario"):
            return fail("Autenticação necessária", 401)
        return fn(*args, **kwargs)
    return wrapped


def current_user():
    user_id = session.get("id_usuario")
    user = users.buscar_por_id(user_id) if user_id else None
    return user.to_dict() if user else None


@api_bp.get("/session")
def get_session():
    return jsonify(user=current_user())


@api_bp.post("/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    try:
        user = users.login_service.executar((data.get("email") or "").strip(), data.get("senha") or "")
        session.clear(); session["id_usuario"] = user.idUsuario
        return jsonify(user=user.to_dict())
    except ValueError as error:
        return fail(error, 401)


@api_bp.post("/auth/register")
def register():
    data = request.get_json(silent=True) or {}
    if data.get("aceitouTermo") is not True:
        return fail("é necessário confirmar a leitura do Termo de Consentimento para criar a conta")
    try:
        user = users.cadastrar_service.executar({"nome": (data.get("nome") or "").strip(), "email": (data.get("email") or "").strip(), "senha": data.get("senha") or ""})
        session.clear(); session["id_usuario"] = user.idUsuario
        return jsonify(user=user.to_dict()), 201
    except ValueError as error:
        return fail(error)


@api_bp.post("/auth/logout")
def logout():
    session.clear()
    return jsonify(message="Sessão encerrada")


@api_bp.get("/trails")
def list_trails():
    query = (request.args.get("q") or "").strip()
    difficulty = (request.args.get("difficulty") or "").strip() or None
    ordering = request.args.get("sort")
    try:
        max_distance = float(request.args["maxDistance"]) if request.args.get("maxDistance") else None
        max_duration = float(request.args["maxDuration"]) if request.args.get("maxDuration") else None
        min_rating = float(request.args["minRating"]) if request.args.get("minRating") else None
    except ValueError:
        return fail("filtros numéricos inválidos")
    if ordering or max_distance is not None or max_duration is not None or min_rating is not None:
        items = trails.listar_ordenadas(ordering, max_distance, max_duration, min_rating)
        if query:
            ids = {t.idTrilha for t in trails.buscar(busca=query)}
            items = [t for t in items if t.idTrilha in ids]
        if difficulty:
            items = [t for t in items if t.dificuldade == difficulty]
    else:
        items = trails.buscar(busca=query or None, dificuldade=difficulty)
    means = trails.medias_avaliacao()
    lat, lon = request.args.get("lat"), request.args.get("lon")
    nearby = {}
    if lat is not None and lon is not None:
        try:
            nearby = {trail.idTrilha: km for trail, km in trails.proximas(float(lat), float(lon), 100)}
            items = [item for item in items if item.idTrilha in nearby]
            items.sort(key=lambda item: nearby[item.idTrilha])
        except ValueError:
            return fail("coordenadas inválidas")
    favorite_ids = {x.idTrilha for x in favorites.listar_por_usuario(session["id_usuario"])} if session.get("id_usuario") else set()
    return jsonify(items=[{**x.to_dict(), "media": means.get(x.idTrilha), "favorito": x.idTrilha in favorite_ids, "distanciaProxima": nearby.get(x.idTrilha)} for x in items])


@api_bp.get("/trails/<int:trail_id>")
def trail_detail(trail_id):
    try:
        trail = trails.buscar_por_id(trail_id)
        reviews = []
        for review in ratings.listar_por_trilha(trail_id):
            author = users.buscar_por_id(review.idUsuario)
            reviews.append({**review.to_dict(), "nomeUsuario": author.nome if author else "Usuário"})
        user_id = session.get("id_usuario")
        favorite = user_id and any(x.idTrilha == trail_id for x in favorites.listar_por_usuario(user_id))
        return jsonify(trail=trail.to_dict(), checkpoints=[x.to_dict() for x in checkpoints.listar_por_trilha(trail_id)], events=[events.to_dict_completo(x) for x in events.listar_por_trilha(trail_id)], reviews=reviews, checklist=[x.to_dict() for x in checklists.listar_por_trilha(trail_id)], favorite=bool(favorite), average=ratings.media_por_trilha(trail_id))
    except ValueError as error:
        return fail(error, 404)


@api_bp.route("/trails/<int:trail_id>/favorite", methods=["POST", "DELETE"])
@authenticated
def favorite_trail(trail_id):
    try:
        if request.method == "POST": favorites.adicionar(session["id_usuario"], trail_id)
        else: favorites.remover(session["id_usuario"], trail_id)
        return jsonify(favorite=request.method == "POST")
    except ValueError as error:
        return fail(error)


@api_bp.get("/favorites")
@authenticated
def list_favorites():
    result = []
    for item in favorites.listar_por_usuario(session["id_usuario"]):
        try: result.append(trails.buscar_por_id(item.idTrilha).to_dict())
        except ValueError: pass
    return jsonify(items=result)


@api_bp.get("/events")
def list_events():
    items = [events.to_dict_completo(x) for x in events.listar_todos()]
    participating = {x.idEvento for x in events.listar_por_usuario(session["id_usuario"])} if session.get("id_usuario") else set()
    return jsonify(items=items, participating=list(participating), trails=[x.to_dict() for x in trails.listar_todos()])


@api_bp.post("/events")
@authenticated
def create_event():
    data = request.get_json(silent=True) or {}
    try:
        day, time = data.get("data"), data.get("horario")
        payload = {"titulo": data.get("titulo", "").strip(), "descricao": data.get("descricao"), "data": datetime.strptime(day, "%Y-%m-%d").date() if day else None, "horarioSaida": datetime.strptime(f"{day} {time}", "%Y-%m-%d %H:%M") if day and time else None, "imediata": bool(data.get("imediata")), "vagas": int(data["vagas"]) if data.get("vagas") else None, "tipo": data.get("tipo", "GRUPO"), "trilhas": [int(data["idTrilha"])] if data.get("idTrilha") else []}
        event = events.criar(session["id_usuario"], payload)
        return jsonify(event=events.to_dict_completo(event)), 201
    except (ValueError, KeyError, TypeError) as error:
        return fail(error)


@api_bp.post("/events/<int:event_id>/participation")
@authenticated
def join_event(event_id):
    try:
        events.entrar(event_id, session["id_usuario"])
        return jsonify(participating=True)
    except ValueError as error:
        return fail(error)


@api_bp.delete("/events/<int:event_id>/participation")
@authenticated
def leave_event(event_id):
    events.sair(event_id, session["id_usuario"])
    return jsonify(participating=False)


@api_bp.post("/trails/<int:trail_id>/reviews")
@authenticated
def create_review(trail_id):
    data = request.get_json(silent=True) or {}
    try:
        ratings.criar(session["id_usuario"], {"idTrilha": trail_id, "nota": data.get("nota"), "comentario": data.get("comentario")})
        return jsonify(message="Avaliação publicada"), 201
    except ValueError as error:
        return fail(error)


@api_bp.route("/reviews/<int:review_id>", methods=["PUT", "DELETE"])
@authenticated
def update_review(review_id):
    try:
        if request.method == "DELETE":
            ratings.deletar(review_id, session["id_usuario"])
            return "", 204
        review = ratings.atualizar(review_id, session["id_usuario"], request.get_json(silent=True) or {})
        return jsonify(review=review.to_dict())
    except PermissionError as error:
        return fail(error, 403)
    except ValueError as error:
        return fail(error, 404 if "não encontrada" in str(error) else 400)


@api_bp.get("/history")
@authenticated
def list_history():
    rows = history.listar_por_usuario(session["id_usuario"])
    result = []
    for row in rows:
        try:
            trail = trails.buscar_por_id(row.idTrilha)
            result.append({**row.to_dict(), "nomeTrilha": trail.nome})
        except ValueError:
            continue
    return jsonify(items=result)


@api_bp.post("/history")
@authenticated
def create_history():
    data = request.get_json(silent=True) or {}
    try:
        if data.get("dataRealizacao"):
            data["dataRealizacao"] = date.fromisoformat(data["dataRealizacao"])
        row = history.criar(session["id_usuario"], data)
        return jsonify(item=row.to_dict()), 201
    except (ValueError, TypeError) as error:
        return fail(error)


@api_bp.patch("/profile")
@authenticated
def update_profile():
    data = request.get_json(silent=True) or {}
    try:
        for key in ("nome", "email", "fotoPerfil"):
            if key in data and isinstance(data[key], str):
                data[key] = data[key].strip()
        user = users.atualizar_perfil(session["id_usuario"], data)
        return jsonify(user=user.to_dict())
    except ValueError as error:
        return fail(error)


@api_bp.post("/events/<int:event_id>/comments")
@authenticated
def comment_event(event_id):
    data = request.get_json(silent=True) or {}
    try:
        comment = events.comentar(event_id, session["id_usuario"], data.get("texto"))
        return jsonify(comment=comment.to_dict()), 201
    except PermissionError as error:
        return fail(error, 403)
    except ValueError as error:
        return fail(error)


@api_bp.route("/events/<int:event_id>", methods=["PUT", "DELETE"])
@authenticated
def manage_event(event_id):
    try:
        if request.method == "DELETE":
            events.deletar(event_id, session["id_usuario"])
            return "", 204
        data = request.get_json(silent=True) or {}
        payload = {}
        if "data" in data:
            payload["data"] = date.fromisoformat(data["data"]) if data["data"] else None
        if "horario" in data:
            payload["horarioSaida"] = datetime.strptime(f"{data.get('data', '')} {data['horario']}", "%Y-%m-%d %H:%M") if data.get("data") and data["horario"] else None
        for key in ("titulo", "descricao", "imediata", "vagas", "tipo"):
            if key in data:
                payload[key] = (int(data[key]) if key == "vagas" and data[key] not in (None, "") else None) if key == "vagas" else data[key]
        event = events.atualizar(event_id, session["id_usuario"], payload)
        return jsonify(event=events.to_dict_completo(event))
    except PermissionError as error:
        return fail(error, 403)
    except (ValueError, TypeError) as error:
        return fail(error)


@api_bp.post("/reports")
@authenticated
def create_report():
    try:
        report = reports.criar(session["id_usuario"], request.get_json(silent=True) or {})
        return jsonify(report=report.to_dict()), 201
    except ValueError as error:
        return fail(error)


def send_recovery_email(email, token):
    host = os.environ.get("SMTP_HOST")
    if not host:
        return False
    message = EmailMessage()
    message["Subject"] = "Recuperação de senha TrailUp"
    message["From"] = os.environ.get("SMTP_FROM", os.environ.get("SMTP_USER", "trailup@localhost"))
    message["To"] = email
    frontend = os.environ.get("FRONTEND_URL", "http://localhost:8000")
    message.set_content(f"Para redefinir sua senha, acesse: {frontend}/?page=reset-password&token={token}\nO link expira em 1 hora.")
    with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", "587")), timeout=10) as server:
        server.starttls()
        if os.environ.get("SMTP_USER"):
            server.login(os.environ["SMTP_USER"], os.environ.get("SMTP_PASSWORD", ""))
        server.send_message(message)
    return True


@api_bp.post("/auth/password-reset")
def request_password_reset():
    email = (request.get_json(silent=True) or {}).get("email", "").strip()
    token = users.solicitar_recuperacao_senha(email)
    if token:
        try:
            sent = send_recovery_email(email, token)
        except (OSError, smtplib.SMTPException) as error:
            return fail(f"não foi possível enviar o e-mail: {error}", 503)
        if not sent and Config.DEBUG:
            return jsonify(message="SMTP não configurado; link disponível apenas em modo de desenvolvimento", resetLink=f"{os.environ.get('FRONTEND_URL', 'http://localhost:8000')}/?page=reset-password&token={token}")
    return jsonify(message="Se o e-mail estiver cadastrado, enviaremos um link de recuperação.")


@api_bp.post("/auth/password-reset/confirm")
def confirm_password_reset():
    data = request.get_json(silent=True) or {}
    try:
        users.redefinir_senha(data.get("token"), data.get("senha", ""))
        return jsonify(message="Senha redefinida com sucesso.")
    except ValueError as error:
        return fail(error)


@api_bp.errorhandler(SQLAlchemyError)
def database_error(error):
    db.session.rollback()
    return fail("Falha ao acessar os dados", 500)
