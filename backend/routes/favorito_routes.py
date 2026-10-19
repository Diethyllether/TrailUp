from flask import Blueprint

from controllers.favorito_controller import FavoritoController
from utils.decorators import login_obrigatorio

favorito_bp = Blueprint("favoritos", __name__)


@favorito_bp.post("/trails/<int:id_trilha>/favorite")
@login_obrigatorio
def adicionar_favorito(id_trilha):
    return FavoritoController.adicionar(id_trilha)


@favorito_bp.delete("/trails/<int:id_trilha>/favorite")
@login_obrigatorio
def remover_favorito(id_trilha):
    return FavoritoController.remover(id_trilha)


@favorito_bp.get("/favorites")
@login_obrigatorio
def listar_favoritos():
    return FavoritoController.listar()
