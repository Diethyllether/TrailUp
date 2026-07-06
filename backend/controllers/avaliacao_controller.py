from flask import Blueprint, request, jsonify

from services.avaliacao_service import AvaliacaoService
from utils.auth import token_obrigatorio

avaliacao_bp = Blueprint("avaliacao_bp", __name__)
service = AvaliacaoService()

@avaliacao_bp.route("/trilhas/<int:id_trilha>/avaliacoes", methods=["GET"])
def listar_por_trilha(id_trilha):
    """Req. 12 - avaliações com nota."""
    avaliacoes = service.listar_por_trilha(id_trilha)
    return jsonify([a.to_dict() for a in avaliacoes]), 200

@avaliacao_bp.route("/trilhas/<int:id_trilha>/avaliacoes", methods=["POST"])
@token_obrigatorio
def criar(id_trilha, id_usuario_logado=None):
    dados = request.get_json() or {}
    dados["idTrilha"] = id_trilha
    try:
        avaliacao = service.criar(id_usuario_logado, dados)
        return jsonify(avaliacao.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@avaliacao_bp.route("/avaliacoes/<int:id_avaliacao>", methods=["PUT"])
@token_obrigatorio
def atualizar(id_avaliacao, id_usuario_logado=None):
    try:
        avaliacao = service.atualizar(id_avaliacao, id_usuario_logado, request.get_json() or {})
        return jsonify(avaliacao.to_dict()), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403

@avaliacao_bp.route("/avaliacoes/<int:id_avaliacao>", methods=["DELETE"])
@token_obrigatorio
def deletar(id_avaliacao, id_usuario_logado=None):
    try:
        service.deletar(id_avaliacao, id_usuario_logado)
        return "", 204
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403
