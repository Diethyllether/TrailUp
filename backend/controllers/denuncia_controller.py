from flask import Blueprint, request, jsonify

from services.denuncia_service import DenunciaService
from utils.auth import token_obrigatorio

denuncia_bp = Blueprint("denuncia_bp", __name__)
service = DenunciaService()

@denuncia_bp.route("/eventos/<int:id_evento>/denuncias", methods=["GET"])
@token_obrigatorio
def listar(id_evento, id_usuario_logado=None):
    """Req. 13 - reportar comportamentos inadequados, com moderação ativa."""
    denuncias = service.listar_por_evento(id_evento)
    return jsonify([d.to_dict() for d in denuncias]), 200

@denuncia_bp.route("/eventos/<int:id_evento>/denuncias", methods=["POST"])
@token_obrigatorio
def criar(id_evento, id_usuario_logado=None):
    dados = request.get_json() or {}
    dados["idEvento"] = id_evento
    try:
        denuncia = service.criar(id_usuario_logado, dados)
        return jsonify(denuncia.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@denuncia_bp.route("/denuncias/<int:id_denuncia>/status", methods=["PUT"])
@token_obrigatorio
def atualizar_status(id_denuncia, id_usuario_logado=None):
    """Ação de moderação (equipe TrailUp analisa e atualiza o status)."""
    status = (request.get_json() or {}).get("status")
    try:
        denuncia = service.atualizar_status(id_denuncia, status)
        return jsonify(denuncia.to_dict()), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
