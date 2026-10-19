from flask import jsonify, session

from services.favorito.adicionar_favorito_service import AdicionarFavoritoService
from services.favorito.listar_favoritos_service import ListarFavoritosService
from services.favorito.remover_favorito_service import RemoverFavoritoService


class FavoritoController:
    @staticmethod
    def adicionar(id_trilha):
        AdicionarFavoritoService().executar(session["id_usuario"], id_trilha)
        return jsonify(favorite=True)

    @staticmethod
    def remover(id_trilha):
        RemoverFavoritoService().executar(session["id_usuario"], id_trilha)
        return jsonify(favorite=False)

    @staticmethod
    def listar():
        itens = ListarFavoritosService().executar(session["id_usuario"])
        return jsonify(items=itens)
