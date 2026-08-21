from flask import Blueprint, request, jsonify

from services.evento_service import EventoService
from services.casos_uso import ListarEventosService, ParticiparEventoService
from utils.auth import token_obrigatorio

evento_bp = Blueprint("evento_bp", __name__)

class EventoController:
    def __init__(self):
        self.service = EventoService()
        self.listar_eventos_service = ListarEventosService()
        self.participar_evento_service = ParticiparEventoService()

    def listar(self):
        apenas_mapa = request.args.get("mapa") == "true"
        eventos = self.listar_eventos_service.executar(apenas_mapa=apenas_mapa)
        return jsonify(
            [self.listar_eventos_service.serializar(e) for e in eventos]
        ), 200

    def buscar(self, id_evento):
        try:
            evento = self.service.buscar_por_id(id_evento)
            return jsonify(self.service.to_dict_completo(evento)), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 404

    @token_obrigatorio
    def criar(self, id_usuario_logado=None):
        try:
            evento = self.service.criar(id_usuario_logado, request.get_json() or {})
            return jsonify(self.service.to_dict_completo(evento)), 201
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    @token_obrigatorio
    def atualizar(self, id_evento, id_usuario_logado=None):
        try:
            evento = self.service.atualizar(
                id_evento, id_usuario_logado, request.get_json() or {}
            )
            return jsonify(self.service.to_dict_completo(evento)), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 404
        except PermissionError as e:
            return jsonify({"erro": str(e)}), 403

    @token_obrigatorio
    def deletar(self, id_evento, id_usuario_logado=None):
        try:
            self.service.deletar(id_evento, id_usuario_logado)
            return "", 204
        except ValueError as e:
            return jsonify({"erro": str(e)}), 404
        except PermissionError as e:
            return jsonify({"erro": str(e)}), 403

    @token_obrigatorio
    def entrar(self, id_evento, id_usuario_logado=None):
        try:
            self.participar_evento_service.executar(id_evento, id_usuario_logado)
            return jsonify({"mensagem": "participação confirmada"}), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    @token_obrigatorio
    def sair(self, id_evento, id_usuario_logado=None):
        self.service.sair(id_evento, id_usuario_logado)
        return jsonify({"mensagem": "você saiu da sala"}), 200

    def listar_participantes(self, id_evento):
        participantes = self.service.listar_participantes(id_evento)
        return jsonify([p.to_dict() for p in participantes]), 200

    def listar_trilhas(self, id_evento):
        vinculos = self.service.listar_trilhas(id_evento)
        return jsonify([v.to_dict() for v in vinculos]), 200

    def listar_por_trilha(self, id_trilha):
        eventos = self.service.listar_por_trilha(id_trilha)
        return jsonify([self.service.to_dict_completo(e) for e in eventos]), 200

controller = EventoController()
evento_bp.add_url_rule("/eventos", "listar", controller.listar, methods=["GET"])
evento_bp.add_url_rule("/eventos/<int:id_evento>", "buscar", controller.buscar, methods=["GET"])
evento_bp.add_url_rule("/eventos", "criar", controller.criar, methods=["POST"])
evento_bp.add_url_rule("/eventos/<int:id_evento>", "atualizar", controller.atualizar, methods=["PUT"])
evento_bp.add_url_rule("/eventos/<int:id_evento>", "deletar", controller.deletar, methods=["DELETE"])
evento_bp.add_url_rule("/eventos/<int:id_evento>/entrar", "entrar", controller.entrar, methods=["POST"])
evento_bp.add_url_rule("/eventos/<int:id_evento>/sair", "sair", controller.sair, methods=["POST"])
evento_bp.add_url_rule(
    "/eventos/<int:id_evento>/participantes",
    "listar_participantes",
    controller.listar_participantes,
    methods=["GET"],
)
evento_bp.add_url_rule(
    "/eventos/<int:id_evento>/trilhas",
    "listar_trilhas",
    controller.listar_trilhas,
    methods=["GET"],
)
evento_bp.add_url_rule(
    "/trilhas/<int:id_trilha>/eventos",
    "listar_por_trilha",
    controller.listar_por_trilha,
    methods=["GET"],
)
