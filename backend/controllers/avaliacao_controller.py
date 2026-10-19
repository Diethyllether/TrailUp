from flask import jsonify, request, session

from services.avaliacao.atualizar_avaliacao_service import AtualizarAvaliacaoService
from services.avaliacao.excluir_avaliacao_service import ExcluirAvaliacaoService
from services.avaliacao.publicar_avaliacao_service import PublicarAvaliacaoService


class AvaliacaoController:
    @staticmethod
    def publicar(id_trilha):
        dados = request.get_json(silent=True) or {}
        PublicarAvaliacaoService().executar(session["id_usuario"], id_trilha, dados)
        return jsonify(message="Avaliação publicada"), 201

    @staticmethod
    def atualizar(id_avaliacao):
        dados = request.get_json(silent=True) or {}
        avaliacao = AtualizarAvaliacaoService().executar(
            id_avaliacao, session["id_usuario"], dados
        )
        return jsonify(review=avaliacao)

    @staticmethod
    def excluir(id_avaliacao):
        ExcluirAvaliacaoService().executar(id_avaliacao, session["id_usuario"])
        return "", 204
