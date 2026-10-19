from flask import jsonify, request, session

from services.relatorio import RankingUsuariosService, ResumoUsuarioService


class RelatorioController:
    @staticmethod
    def ranking_usuarios():
        items = RankingUsuariosService().executar(request.args.get("limite", 10))
        return jsonify(items=items)

    @staticmethod
    def resumo_usuario():
        item = ResumoUsuarioService().executar(session["id_usuario"])
        return jsonify(item=item)
