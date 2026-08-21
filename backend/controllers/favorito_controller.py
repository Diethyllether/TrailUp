from flask import Blueprint, request, jsonify

from services.casos_uso import (
    AdicionarFavoritoService,
    ListarFavoritosService,
    RemoverFavoritoService,
)
from utils.auth import token_obrigatorio

favorito_bp = Blueprint("favorito_bp", __name__)

class FavoritoController:
    def __init__(self):
        self.listar_service = ListarFavoritosService()
        self.adicionar_service = AdicionarFavoritoService()
        self.remover_service = RemoverFavoritoService()

    @token_obrigatorio
    def listar(self, id_usuario, id_usuario_logado=None):
        if id_usuario_logado != id_usuario:
            return jsonify({"erro": "você só pode consultar os próprios favoritos"}), 403
        favoritos = self.listar_service.executar(id_usuario)
        return jsonify([f.to_dict() for f in favoritos]), 200

    @token_obrigatorio
    def adicionar(self, id_usuario_logado=None):
        dados = request.get_json() or {}
        if not dados.get("idTrilha"):
            return jsonify({"erro": "idTrilha é obrigatório"}), 400
        favorito = self.adicionar_service.executar(
            id_usuario_logado, dados["idTrilha"]
        )
        return jsonify(favorito.to_dict()), 201

    @token_obrigatorio
    def remover(self, id_trilha, id_usuario_logado=None):
        try:
            self.remover_service.executar(id_usuario_logado, id_trilha)
            return "", 204
        except ValueError as e:
            return jsonify({"erro": str(e)}), 404

controller = FavoritoController()
favorito_bp.add_url_rule(
    "/usuarios/<int:id_usuario>/favoritos",
    "listar",
    controller.listar,
    methods=["GET"],
)
favorito_bp.add_url_rule("/favoritos", "adicionar", controller.adicionar, methods=["POST"])
favorito_bp.add_url_rule(
    "/favoritos/<int:id_trilha>",
    "remover",
    controller.remover,
    methods=["DELETE"],
)
