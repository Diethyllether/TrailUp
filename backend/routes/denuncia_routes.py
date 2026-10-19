from flask import Blueprint

from controllers.denuncia_controller import DenunciaController
from utils.decorators import login_obrigatorio

denuncia_bp = Blueprint("denuncias", __name__)


@denuncia_bp.post("/reports")
@login_obrigatorio
def reportar_problema():
    return DenunciaController.reportar()
