from flask import Blueprint, request, jsonify

from services.historico_service import HistoricoService
from utils.auth import token_obrigatorio

historico_bp = Blueprint("historico_bp", __name__)
service = HistoricoService()

@historico_bp.route("/usuarios/<int:id_usuario>/historico", methods=["GET"])
@token_obrigatorio
def listar(id_usuario, id_usuario_logado=None):
    """Req. 18 - histórico de trilhas realizadas."""
    if id_usuario != id_usuario_logado:
        return jsonify({"erro": "você só pode ver o próprio histórico"}), 403
    historico = service.listar_por_usuario(id_usuario)
    return jsonify([h.to_dict() for h in historico]), 200

@historico_bp.route("/historico", methods=["POST"])
@token_obrigatorio
def criar(id_usuario_logado=None):
    try:
        historico = service.criar(id_usuario_logado, request.get_json() or {})
        return jsonify(historico.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@historico_bp.route("/historico/<int:id_historico>/registros", methods=["GET"])
def listar_registros(id_historico):
    """Req. 16 - checkpoints via GPS durante a realização da trilha."""
    registros = service.listar_registros(id_historico)
    return jsonify([r.to_dict() for r in registros]), 200

@historico_bp.route("/historico/<int:id_historico>/registros", methods=["POST"])
@token_obrigatorio
def registrar_checkpoint(id_historico, id_usuario_logado=None):
    try:
        registro = service.registrar_checkpoint(id_historico, request.get_json() or {})
        return jsonify(registro.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@historico_bp.route("/registros/<int:id_registro>/fotos", methods=["GET"])
def listar_fotos_registro(id_registro):
    fotos = service.listar_fotos_registro(id_registro)
    return jsonify([f.to_dict() for f in fotos]), 200

@historico_bp.route("/registros/<int:id_registro>/fotos", methods=["POST"])
@token_obrigatorio
def anexar_foto(id_registro, id_usuario_logado=None):
    """Fotos vinculadas ao ponto da trilha (câmera contextual do checkpoint)."""
    try:
        foto = service.anexar_foto_registro(id_registro, request.get_json() or {})
        return jsonify(foto.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
