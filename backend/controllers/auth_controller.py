from flask import jsonify, request, session

from services.usuario.autenticar_usuario_service import AutenticarUsuarioService
from services.usuario.cadastrar_usuario_service import CadastrarUsuarioService
from services.usuario.consultar_sessao_service import ConsultarSessaoService
from services.usuario.encerrar_sessao_service import EncerrarSessaoService
from services.usuario.redefinir_senha_service import RedefinirSenhaService
from services.usuario.solicitar_recuperacao_senha_service import SolicitarRecuperacaoSenhaService


class AuthController:
    @staticmethod
    def consultar_sessao():
        usuario = ConsultarSessaoService().executar(session.get("id_usuario"))
        return jsonify(user=usuario)

    @staticmethod
    def autenticar():
        dados = request.get_json(silent=True) or {}
        usuario = AutenticarUsuarioService().executar(dados.get("email"), dados.get("senha"))
        session.clear()
        session["id_usuario"] = usuario["idUsuario"]
        return jsonify(user=usuario)

    @staticmethod
    def cadastrar():
        dados = request.get_json(silent=True) or {}
        usuario = CadastrarUsuarioService().executar(dados)
        session.clear()
        session["id_usuario"] = usuario["idUsuario"]
        return jsonify(user=usuario), 201

    @staticmethod
    def encerrar_sessao():
        resposta = EncerrarSessaoService().executar()
        session.clear()
        return jsonify(**resposta)

    @staticmethod
    def solicitar_recuperacao():
        dados = request.get_json(silent=True) or {}
        SolicitarRecuperacaoSenhaService().executar((dados.get("email") or "").strip())
        return jsonify(
            message="Se o e-mail estiver cadastrado, enviaremos um link de recuperação."
        )

    @staticmethod
    def redefinir_senha():
        dados = request.get_json(silent=True) or {}
        RedefinirSenhaService().executar(dados.get("token"), dados.get("senha", ""))
        return jsonify(message="Senha redefinida com sucesso.")
