from flask import Blueprint

from controllers.historico_controller import HistoricoController
from utils.decorators import login_obrigatorio

historico_bp = Blueprint("historico", __name__)


@historico_bp.get("/history")
@login_obrigatorio
def consultar_historico():
    return HistoricoController.consultar()


@historico_bp.post("/history")
@login_obrigatorio
def registrar_trilha():
    return HistoricoController.registrar()
