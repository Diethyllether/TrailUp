from flask import Blueprint, request, jsonify

from services.checkpoint_service import CheckpointService
from utils.auth import token_obrigatorio

checkpoint_bp = Blueprint("checkpoint_bp", __name__)
service = CheckpointService()

@checkpoint_bp.route("/trilhas/<int:id_trilha>/checkpoints", methods=["GET"])
def listar(id_trilha):
    """Req. 9 - pontos exibidos no mapa da trilha."""
    checkpoints = service.listar_por_trilha(id_trilha)
    return jsonify([c.to_dict() for c in checkpoints]), 200

@checkpoint_bp.route("/trilhas/<int:id_trilha>/checkpoints", methods=["POST"])
@token_obrigatorio
def criar(id_trilha, id_usuario_logado=None):
    dados = request.get_json() or {}
    dados["idTrilha"] = id_trilha
    try:
        checkpoint = service.criar(dados)
        return jsonify(checkpoint.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@checkpoint_bp.route("/checkpoints/<int:id_checkpoint>", methods=["DELETE"])
@token_obrigatorio
def deletar(id_checkpoint, id_usuario_logado=None):
    try:
        service.deletar(id_checkpoint)
        return "", 204
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
