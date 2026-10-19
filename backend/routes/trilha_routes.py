from flask import Blueprint

from controllers.trilha_controller import TrilhaController

trilha_bp = Blueprint("trilhas", __name__)


@trilha_bp.get("/trails")
def buscar_trilhas():
    return TrilhaController.buscar()


@trilha_bp.get("/trails/<int:id_trilha>")
def detalhar_trilha(id_trilha):
    return TrilhaController.detalhar(id_trilha)
