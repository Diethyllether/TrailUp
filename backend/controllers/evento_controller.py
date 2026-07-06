from flask import Blueprint, request, jsonify

from services.evento_service import EventoService
from utils.auth import token_obrigatorio

evento_bp = Blueprint("evento_bp", __name__)
service = EventoService()

@evento_bp.route("/eventos", methods=["GET"])
def listar():
    """
    Req. 17 - listar salas/eventos de trilha.
    ?mapa=true retorna somente salas com coordenadas, para exibir como
    pins em tempo real no mapa (vide descrição do produto).
    """
    if request.args.get("mapa") == "true":
        eventos = service.listar_ativos_no_mapa()
    else:
        eventos = service.listar_todos()
    return jsonify([service.to_dict_completo(e) for e in eventos]), 200

@evento_bp.route("/eventos/<int:id_evento>", methods=["GET"])
def buscar(id_evento):
    try:
        evento = service.buscar_por_id(id_evento)
        return jsonify(service.to_dict_completo(evento)), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404

@evento_bp.route("/eventos", methods=["POST"])
@token_obrigatorio
def criar(id_usuario_logado=None):
    try:
        evento = service.criar(id_usuario_logado, request.get_json() or {})
        return jsonify(service.to_dict_completo(evento)), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@evento_bp.route("/eventos/<int:id_evento>", methods=["PUT"])
@token_obrigatorio
def atualizar(id_evento, id_usuario_logado=None):
    try:
        evento = service.atualizar(id_evento, id_usuario_logado, request.get_json() or {})
        return jsonify(service.to_dict_completo(evento)), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403

@evento_bp.route("/eventos/<int:id_evento>", methods=["DELETE"])
@token_obrigatorio
def deletar(id_evento, id_usuario_logado=None):
    try:
        service.deletar(id_evento, id_usuario_logado)
        return "", 204
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403

@evento_bp.route("/eventos/<int:id_evento>/entrar", methods=["POST"])
@token_obrigatorio
def entrar(id_evento, id_usuario_logado=None):
    try:
        service.entrar(id_evento, id_usuario_logado)
        return jsonify({"mensagem": "participação confirmada"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@evento_bp.route("/eventos/<int:id_evento>/sair", methods=["POST"])
@token_obrigatorio
def sair(id_evento, id_usuario_logado=None):
    service.sair(id_evento, id_usuario_logado)
    return jsonify({"mensagem": "você saiu da sala"}), 200

@evento_bp.route("/eventos/<int:id_evento>/participantes", methods=["GET"])
def listar_participantes(id_evento):
    participantes = service.listar_participantes(id_evento)
    return jsonify([p.to_dict() for p in participantes]), 200

@evento_bp.route("/eventos/<int:id_evento>/trilhas", methods=["GET"])
def listar_trilhas(id_evento):
    vinculos = service.listar_trilhas(id_evento)
    return jsonify([v.to_dict() for v in vinculos]), 200

@evento_bp.route("/trilhas/<int:id_trilha>/eventos", methods=["GET"])
def listar_por_trilha(id_trilha):
    """Expedições/salas vinculadas a uma trilha específica (usado na tela
    de detalhe da trilha no app)."""
    eventos = service.listar_por_trilha(id_trilha)
    return jsonify([service.to_dict_completo(e) for e in eventos]), 200
