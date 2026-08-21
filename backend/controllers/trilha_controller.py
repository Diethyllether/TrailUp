from flask import Blueprint, request, jsonify

from services.trilha_service import TrilhaService
from services.casos_uso import BuscarTrilhasService, DetalharTrilhaService
from utils.auth import token_obrigatorio

trilha_bp = Blueprint("trilha_bp", __name__)

class TrilhaController:
    def __init__(self):
        self.service = TrilhaService()
        self.buscar_trilhas_service = BuscarTrilhasService()
        self.detalhar_trilha_service = DetalharTrilhaService()

    def listar(self):
        trilhas = self.buscar_trilhas_service.executar(
            nome=request.args.get("nome"),
            localizacao=request.args.get("localizacao"),
            dificuldade=request.args.get("dificuldade"),
            busca=request.args.get("busca"),
        )
        return jsonify([t.to_dict() for t in trilhas]), 200

    def buscar(self, id_trilha):
        try:
            trilha = self.detalhar_trilha_service.executar(id_trilha)
            return jsonify(trilha.to_dict()), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 404

    @token_obrigatorio
    def criar(self, id_usuario_logado=None):
        try:
            trilha = self.service.criar(request.get_json() or {})
            return jsonify(trilha.to_dict()), 201
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    @token_obrigatorio
    def atualizar(self, id_trilha, id_usuario_logado=None):
        try:
            trilha = self.service.atualizar(id_trilha, request.get_json() or {})
            return jsonify(trilha.to_dict()), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    @token_obrigatorio
    def deletar(self, id_trilha, id_usuario_logado=None):
        try:
            self.service.deletar(id_trilha)
            return "", 204
        except ValueError as e:
            return jsonify({"erro": str(e)}), 404

controller = TrilhaController()
trilha_bp.add_url_rule("/trilhas", "listar", controller.listar, methods=["GET"])
trilha_bp.add_url_rule("/trilhas/<int:id_trilha>", "buscar", controller.buscar, methods=["GET"])
trilha_bp.add_url_rule("/trilhas", "criar", controller.criar, methods=["POST"])
trilha_bp.add_url_rule("/trilhas/<int:id_trilha>", "atualizar", controller.atualizar, methods=["PUT"])
trilha_bp.add_url_rule("/trilhas/<int:id_trilha>", "deletar", controller.deletar, methods=["DELETE"])
