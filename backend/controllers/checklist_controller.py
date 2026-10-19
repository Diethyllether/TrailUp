from flask import jsonify, request, session

from services.checklist.consultar_checklist_service import ConsultarChecklistService
from services.checklist.marcar_item_checklist_service import MarcarItemChecklistService


class ChecklistController:
    @staticmethod
    def consultar(id_trilha):
        dados = ConsultarChecklistService().executar(session["id_usuario"], id_trilha)
        return jsonify(**dados)

    @staticmethod
    def marcar(id_item):
        dados = request.get_json(silent=True) or {}
        item = MarcarItemChecklistService().executar(
            session["id_usuario"], id_item, dados.get("marcado")
        )
        return jsonify(item=item)
