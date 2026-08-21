from flask import Blueprint, request, jsonify

from services.usuario_service import UsuarioService
from services.casos_uso import (
    AtualizarPerfilService,
    CadastrarUsuarioService,
    LoginUsuarioService,
)
from utils.auth import token_obrigatorio

usuario_bp = Blueprint("usuario_bp", __name__)

class UsuarioController:
    def __init__(self):
        self.service = UsuarioService()
        self.cadastrar_service = CadastrarUsuarioService()
        self.login_service = LoginUsuarioService()
        self.atualizar_perfil_service = AtualizarPerfilService()

    def cadastrar(self):
        try:
            usuario = self.cadastrar_service.executar(request.get_json() or {})
            return jsonify(usuario.to_dict()), 201
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    def login(self):
        dados = request.get_json() or {}
        try:
            token, usuario = self.login_service.executar(
                dados.get("email"), dados.get("senha")
            )
            return jsonify({"token": token, "usuario": usuario.to_dict()}), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 401

    def solicitar_recuperacao(self):
        email = (request.get_json() or {}).get("email")
        token = self.service.solicitar_recuperacao_senha(email)
        resposta = {"mensagem": "se o email existir, um link de recuperação foi enviado"}
        if token:
            resposta["token_debug"] = token
        return jsonify(resposta), 200

    def redefinir_senha(self):
        dados = request.get_json() or {}
        try:
            self.service.redefinir_senha(dados.get("token"), dados.get("novaSenha"))
            return jsonify({"mensagem": "senha redefinida com sucesso"}), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    def listar(self):
        usuarios = self.service.listar_todos()
        return jsonify([u.to_dict() for u in usuarios]), 200

    def buscar(self, id_usuario):
        try:
            usuario = self.service.buscar_por_id(id_usuario)
            return jsonify(usuario.to_dict()), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 404

    @token_obrigatorio
    def atualizar(self, id_usuario, id_usuario_logado=None):
        if id_usuario_logado != id_usuario:
            return jsonify({"erro": "você só pode editar o próprio perfil"}), 403
        try:
            usuario = self.atualizar_perfil_service.executar(
                id_usuario, request.get_json() or {}
            )
            return jsonify(usuario.to_dict()), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    @token_obrigatorio
    def deletar(self, id_usuario, id_usuario_logado=None):
        if id_usuario_logado != id_usuario:
            return jsonify({"erro": "você só pode remover o próprio perfil"}), 403
        try:
            self.service.deletar(id_usuario)
            return "", 204
        except ValueError as e:
            return jsonify({"erro": str(e)}), 404

controller = UsuarioController()
usuario_bp.add_url_rule("/usuarios", "cadastrar", controller.cadastrar, methods=["POST"])
usuario_bp.add_url_rule("/login", "login", controller.login, methods=["POST"])
usuario_bp.add_url_rule("/recuperar-senha", "solicitar_recuperacao", controller.solicitar_recuperacao, methods=["POST"])
usuario_bp.add_url_rule("/redefinir-senha", "redefinir_senha", controller.redefinir_senha, methods=["POST"])
usuario_bp.add_url_rule("/usuarios", "listar", controller.listar, methods=["GET"])
usuario_bp.add_url_rule("/usuarios/<int:id_usuario>", "buscar", controller.buscar, methods=["GET"])
usuario_bp.add_url_rule("/usuarios/<int:id_usuario>", "atualizar", controller.atualizar, methods=["PUT"])
usuario_bp.add_url_rule("/usuarios/<int:id_usuario>", "deletar", controller.deletar, methods=["DELETE"])
