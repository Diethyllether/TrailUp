from flask import Blueprint

from controllers.usuario_controller import UsuarioController
from utils.decorators import login_obrigatorio

usuario_bp = Blueprint("usuario", __name__)


@usuario_bp.patch("/profile")
@login_obrigatorio
def atualizar_perfil():
    return UsuarioController.atualizar_perfil()


@usuario_bp.get("/profile/export")
@login_obrigatorio
def exportar_dados():
    return UsuarioController.exportar_dados()
