from flask import Blueprint, request, jsonify

from services.favorito_service import FavoritoService
from utils.auth import token_obrigatorio

favorito_bp = Blueprint("favorito_bp", __name__)
service = FavoritoService()

@favorito_bp.route("/usuarios/<int:id_usuario>/favoritos", methods=["GET"])
@token_obrigatorio
def listar(id_usuario, id_usuario_logado=None):
    """Req. 14 - salvar trilhas como favoritas."""
    favoritos = service.listar_por_usuario(id_usuario)
    return jsonify([f.to_dict() for f in favoritos]), 200

@favorito_bp.route("/favoritos", methods=["POST"])
@token_obrigatorio
def adicionar(id_usuario_logado=None):
    dados = request.get_json() or {}
    if not dados.get("idTrilha"):
        return jsonify({"erro": "idTrilha é obrigatório"}), 400
    favorito = service.adicionar(id_usuario_logado, dados["idTrilha"])
    return jsonify(favorito.to_dict()), 201

@favorito_bp.route("/favoritos/<int:id_trilha>", methods=["DELETE"])
@token_obrigatorio
def remover(id_trilha, id_usuario_logado=None):
    try:
        service.remover(id_usuario_logado, id_trilha)
        return "", 204
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
