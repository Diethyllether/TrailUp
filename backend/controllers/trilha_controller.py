from flask import Blueprint, request, jsonify

from services.trilha_service import TrilhaService
from utils.auth import token_obrigatorio

trilha_bp = Blueprint("trilha_bp", __name__)
service = TrilhaService()

@trilha_bp.route("/trilhas", methods=["GET"])
def listar():
    """Req. 5, 6, 8 - busca por nome/localização e filtro por dificuldade."""
    nome = request.args.get("nome")
    localizacao = request.args.get("localizacao")
    dificuldade = request.args.get("dificuldade")
    busca = request.args.get("busca")

    if nome or localizacao or dificuldade or busca:
        trilhas = service.buscar(nome=nome, localizacao=localizacao, dificuldade=dificuldade, busca=busca)
    else:
        trilhas = service.listar_todos()
    return jsonify([t.to_dict() for t in trilhas]), 200

@trilha_bp.route("/trilhas/<int:id_trilha>", methods=["GET"])
def buscar(id_trilha):
    try:
        trilha = service.buscar_por_id(id_trilha)
        return jsonify(trilha.to_dict()), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404

@trilha_bp.route("/trilhas", methods=["POST"])
@token_obrigatorio
def criar(id_usuario_logado=None):
    try:
        trilha = service.criar(request.get_json() or {})
        return jsonify(trilha.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@trilha_bp.route("/trilhas/<int:id_trilha>", methods=["PUT"])
@token_obrigatorio
def atualizar(id_trilha, id_usuario_logado=None):
    try:
        trilha = service.atualizar(id_trilha, request.get_json() or {})
        return jsonify(trilha.to_dict()), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@trilha_bp.route("/trilhas/<int:id_trilha>", methods=["DELETE"])
@token_obrigatorio
def deletar(id_trilha, id_usuario_logado=None):
    try:
        service.deletar(id_trilha)
        return "", 204
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
