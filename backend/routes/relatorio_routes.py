from flask import Blueprint

from controllers.relatorio_controller import RelatorioController

relatorio_bp = Blueprint("relatorios", __name__)


@relatorio_bp.get("/reports/ranking")
def ranking_usuarios():
    return RelatorioController.ranking_usuarios()


@relatorio_bp.get("/reports/summary")
def resumo_usuario():
    return RelatorioController.resumo_usuario()
