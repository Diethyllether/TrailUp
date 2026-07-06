from flask import Blueprint, request, jsonify

from services.mapa_offline_service import MapaOfflineService
from utils.auth import token_obrigatorio

mapa_offline_bp = Blueprint("mapa_offline_bp", __name__)
service = MapaOfflineService()

@mapa_offline_bp.route("/trilhas/<int:id_trilha>/mapas-offline", methods=["GET"])
def listar(id_trilha):
    """Req. 10 - download de mapas offline."""
    mapas = service.listar_por_trilha(id_trilha)
    return jsonify([m.to_dict() for m in mapas]), 200

@mapa_offline_bp.route("/trilhas/<int:id_trilha>/mapas-offline", methods=["POST"])
@token_obrigatorio
def registrar_download(id_trilha, id_usuario_logado=None):
    dados = request.get_json() or {}
    dados["idTrilha"] = id_trilha
    try:
        mapa = service.registrar_download(dados)
        return jsonify(mapa.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@mapa_offline_bp.route("/mapas-offline/<int:id_mapa>", methods=["DELETE"])
@token_obrigatorio
def deletar(id_mapa, id_usuario_logado=None):
    try:
        service.deletar(id_mapa)
        return "", 204
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
