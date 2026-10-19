from flask import jsonify, request, session

from services.relatorio import RankingUsuariosService, ResumoUsuarioService


class RelatorioController:
    @staticmethod
    def ranking_usuarios():
        try:
            items = RankingUsuariosService().executar(request.args.get("limite", 10))
            return jsonify(items=items)
        except ValueError as error:
            return jsonify(error=str(error)), 400

    @staticmethod
    def resumo_usuario():
        if not session.get("id_usuario"):
            return jsonify(error="Autenticação necessária"), 401
        try:
            item = ResumoUsuarioService().executar(session["id_usuario"])
            return jsonify(item=item)
        except ValueError as error:
            return jsonify(error=str(error)), 404
