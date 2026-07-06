from flask import Blueprint, request, jsonify

from services.usuario_service import UsuarioService
from utils.auth import token_obrigatorio

usuario_bp = Blueprint("usuario_bp", __name__)
service = UsuarioService()

@usuario_bp.route("/usuarios", methods=["POST"])
def cadastrar():
    """Req. 1 - cadastro de usuários."""
    try:
        usuario = service.cadastrar(request.get_json() or {})
        return jsonify(usuario.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@usuario_bp.route("/login", methods=["POST"])
def login():
    """Req. 2 - login de usuários."""
    dados = request.get_json() or {}
    try:
        token, usuario = service.login(dados.get("email"), dados.get("senha"))
        return jsonify({"token": token, "usuario": usuario.to_dict()}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 401

@usuario_bp.route("/recuperar-senha", methods=["POST"])
def solicitar_recuperacao():
    """Req. 3 - recuperação de senha (etapa 1: gera token)."""
    email = (request.get_json() or {}).get("email")
    token = service.solicitar_recuperacao_senha(email)
    resposta = {"mensagem": "se o email existir, um link de recuperação foi enviado"}
    if token:
        resposta["token_debug"] = token
    return jsonify(resposta), 200

@usuario_bp.route("/redefinir-senha", methods=["POST"])
def redefinir_senha():
    """Req. 3 - recuperação de senha (etapa 2: redefine com o token)."""
    dados = request.get_json() or {}
    try:
        service.redefinir_senha(dados.get("token"), dados.get("novaSenha"))
        return jsonify({"mensagem": "senha redefinida com sucesso"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@usuario_bp.route("/usuarios", methods=["GET"])
def listar():
    usuarios = service.listar_todos()
    return jsonify([u.to_dict() for u in usuarios]), 200

@usuario_bp.route("/usuarios/<int:id_usuario>", methods=["GET"])
def buscar(id_usuario):
    try:
        usuario = service.buscar_por_id(id_usuario)
        return jsonify(usuario.to_dict()), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404

@usuario_bp.route("/usuarios/<int:id_usuario>", methods=["PUT"])
@token_obrigatorio
def atualizar(id_usuario, id_usuario_logado=None):
    """Req. 4 - edição de perfil."""
    if id_usuario_logado != id_usuario:
        return jsonify({"erro": "você só pode editar o próprio perfil"}), 403
    try:
        usuario = service.atualizar_perfil(id_usuario, request.get_json() or {})
        return jsonify(usuario.to_dict()), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@usuario_bp.route("/usuarios/<int:id_usuario>", methods=["DELETE"])
@token_obrigatorio
def deletar(id_usuario, id_usuario_logado=None):
    if id_usuario_logado != id_usuario:
        return jsonify({"erro": "você só pode remover o próprio perfil"}), 403
    try:
        service.deletar(id_usuario)
        return "", 204
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
