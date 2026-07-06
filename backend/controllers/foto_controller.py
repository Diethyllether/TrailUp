from flask import Blueprint, request, jsonify

from services.foto_service import FotoService
from utils.auth import token_obrigatorio

foto_bp = Blueprint("foto_bp", __name__)
service = FotoService()

@foto_bp.route("/trilhas/<int:id_trilha>/fotos", methods=["GET"])
def listar(id_trilha):
    """Req. 7 - exibir imagens das trilhas."""
    fotos = service.listar_por_trilha(id_trilha)
    return jsonify([f.to_dict() for f in fotos]), 200

@foto_bp.route("/trilhas/<int:id_trilha>/fotos", methods=["POST"])
@token_obrigatorio
def criar(id_trilha, id_usuario_logado=None):
    dados = request.get_json() or {}
    dados["idTrilha"] = id_trilha
    try:
        foto = service.criar(dados)
        return jsonify(foto.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@foto_bp.route("/fotos/<int:id_foto>", methods=["DELETE"])
@token_obrigatorio
def deletar(id_foto, id_usuario_logado=None):
    try:
        service.deletar(id_foto)
        return "", 204
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
