from flask import Blueprint

from controllers.avaliacao_controller import AvaliacaoController
from utils.decorators import login_obrigatorio

avaliacao_bp = Blueprint("avaliacoes", __name__)


@avaliacao_bp.post("/trails/<int:id_trilha>/reviews")
@login_obrigatorio
def publicar_avaliacao(id_trilha):
    return AvaliacaoController.publicar(id_trilha)


@avaliacao_bp.put("/reviews/<int:id_avaliacao>")
@login_obrigatorio
def atualizar_avaliacao(id_avaliacao):
    return AvaliacaoController.atualizar(id_avaliacao)


@avaliacao_bp.delete("/reviews/<int:id_avaliacao>")
@login_obrigatorio
def excluir_avaliacao(id_avaliacao):
    return AvaliacaoController.excluir(id_avaliacao)
