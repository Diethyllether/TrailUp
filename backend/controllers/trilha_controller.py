from flask import jsonify, request, session

from services.trilha.buscar_trilhas_service import BuscarTrilhasService
from services.trilha.detalhar_trilha_service import DetalharTrilhaService


class TrilhaController:
    @staticmethod
    def buscar():
        itens = BuscarTrilhasService().executar(
            termo=request.args.get("q"),
            dificuldade=request.args.get("difficulty"),
            distancia_max=request.args.get("maxDistance"),
            duracao_max=request.args.get("maxDuration"),
            nota_min=request.args.get("minRating"),
            ordem=request.args.get("sort"),
            latitude=request.args.get("lat"),
            longitude=request.args.get("lon"),
            id_usuario=session.get("id_usuario"),
        )
        return jsonify(items=itens)

    @staticmethod
    def detalhar(id_trilha):
        dados = DetalharTrilhaService().executar(id_trilha, session.get("id_usuario"))
        return jsonify(**dados)
