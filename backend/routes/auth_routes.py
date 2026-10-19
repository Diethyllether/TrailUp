from flask import Blueprint

from controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/session")
def consultar_sessao():
    return AuthController.consultar_sessao()


@auth_bp.post("/auth/login")
def autenticar():
    return AuthController.autenticar()


@auth_bp.post("/auth/register")
def cadastrar():
    return AuthController.cadastrar()


@auth_bp.post("/auth/logout")
def encerrar_sessao():
    return AuthController.encerrar_sessao()


@auth_bp.post("/auth/password-reset")
def solicitar_recuperacao():
    return AuthController.solicitar_recuperacao()


@auth_bp.post("/auth/password-reset/confirm")
def redefinir_senha():
    return AuthController.redefinir_senha()
