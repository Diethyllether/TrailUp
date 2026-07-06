from flask import Blueprint, request, jsonify

from services.notificacao_service import NotificacaoService
from utils.auth import token_obrigatorio

notificacao_bp = Blueprint("notificacao_bp", __name__)
service = NotificacaoService()

@notificacao_bp.route("/usuarios/<int:id_usuario>/notificacoes", methods=["GET"])
@token_obrigatorio
def listar(id_usuario, id_usuario_logado=None):
    """Req. 19 - notificações ao usuário."""
    if id_usuario != id_usuario_logado:
        return jsonify({"erro": "você só pode ver suas próprias notificações"}), 403
    apenas_nao_lidas = request.args.get("naoLidas") == "true"
    notificacoes = service.listar_por_usuario(id_usuario, apenas_nao_lidas)
    return jsonify([n.to_dict() for n in notificacoes]), 200

@notificacao_bp.route("/notificacoes", methods=["POST"])
@token_obrigatorio
def criar(id_usuario_logado=None):
    try:
        notificacao = service.criar(request.get_json() or {})
        return jsonify(notificacao.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@notificacao_bp.route("/notificacoes/<int:id_notificacao>/lida", methods=["PUT"])
@token_obrigatorio
def marcar_como_lida(id_notificacao, id_usuario_logado=None):
    try:
        notificacao = service.marcar_como_lida(id_notificacao, id_usuario_logado)
        return jsonify(notificacao.to_dict()), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
