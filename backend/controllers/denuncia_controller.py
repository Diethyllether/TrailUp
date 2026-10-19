from flask import jsonify, request, session

from services.denuncia.reportar_problema_service import ReportarProblemaService


class DenunciaController:
    @staticmethod
    def reportar():
        dados = request.get_json(silent=True) or {}
        denuncia = ReportarProblemaService().executar(session["id_usuario"], dados)
        return jsonify(report=denuncia), 201
