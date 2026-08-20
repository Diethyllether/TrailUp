from flask import Blueprint, jsonify, request

from services.relatorio_service import RelatorioService
from utils.auth import token_obrigatorio


relatorio_bp = Blueprint("relatorio_bp", __name__)
service = RelatorioService()


@relatorio_bp.route("/relatorios/trilhas", methods=["GET"])
def trilhas_ordenadas():
    try:
        resultado = service.trilhas_ordenadas(
            dificuldade=request.args.get("dificuldade"),
            localizacao=request.args.get("localizacao"),
            ordem=request.args.get("ordem", "nota"),
        )
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@relatorio_bp.route("/relatorios/usuarios/<int:id_usuario>/favoritos", methods=["GET"])
@token_obrigatorio
def favoritos_usuario(id_usuario, id_usuario_logado=None):
    if id_usuario_logado != id_usuario:
        return jsonify({"erro": "você só pode consultar os próprios favoritos"}), 403
    return jsonify(service.favoritos_usuario(id_usuario)), 200


@relatorio_bp.route("/relatorios/usuarios/<int:id_usuario>/resumo", methods=["GET"])
@token_obrigatorio
def resumo_usuario(id_usuario, id_usuario_logado=None):
    if id_usuario_logado != id_usuario:
        return jsonify({"erro": "você só pode consultar o próprio resumo"}), 403
    try:
        return jsonify(service.resumo_usuario(id_usuario)), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@relatorio_bp.route("/relatorios/usuarios/ranking", methods=["GET"])
def ranking_usuarios():
    try:
        return jsonify(service.ranking_usuarios(request.args.get("limite", 10))), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
