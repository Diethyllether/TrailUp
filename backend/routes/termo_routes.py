from flask import Blueprint

from controllers.termo_controller import TermoController

termo_bp = Blueprint("termo", __name__)


@termo_bp.get("/termo-consentimento")
def servir_termo():
    return TermoController.servir()
