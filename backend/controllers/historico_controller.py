from flask import jsonify, request, session

from services.historico.consultar_historico_service import ConsultarHistoricoService
from services.historico.registrar_trilha_concluida_service import RegistrarTrilhaConcluidaService


class HistoricoController:
    @staticmethod
    def consultar():
        itens = ConsultarHistoricoService().executar(session["id_usuario"])
        return jsonify(items=itens)

    @staticmethod
    def registrar():
        dados = request.get_json(silent=True) or {}
        item = RegistrarTrilhaConcluidaService().executar(session["id_usuario"], dados)
        return jsonify(item=item), 201
