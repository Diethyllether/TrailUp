from flask import jsonify, request, session

from services.evento.atualizar_evento_service import AtualizarEventoService
from services.evento.cancelar_evento_service import CancelarEventoService
from services.evento.comentar_evento_service import ComentarEventoService
from services.evento.criar_evento_service import CriarEventoService
from services.evento.listar_eventos_ativos_service import ListarEventosAtivosService
from services.evento.participar_evento_service import ParticiparEventoService
from services.evento.sair_evento_service import SairEventoService


class EventoController:
    @staticmethod
    def listar():
        dados = ListarEventosAtivosService().executar(session.get("id_usuario"))
        return jsonify(**dados)

    @staticmethod
    def criar():
        dados = request.get_json(silent=True) or {}
        evento = CriarEventoService().executar(session["id_usuario"], dados)
        return jsonify(event=evento), 201

    @staticmethod
    def participar(id_evento):
        dados = ParticiparEventoService().executar(id_evento, session["id_usuario"])
        return jsonify(**dados)

    @staticmethod
    def sair(id_evento):
        dados = SairEventoService().executar(id_evento, session["id_usuario"])
        return jsonify(**dados)

    @staticmethod
    def atualizar(id_evento):
        dados = request.get_json(silent=True) or {}
        evento = AtualizarEventoService().executar(
            id_evento, session["id_usuario"], dados
        )
        return jsonify(event=evento)

    @staticmethod
    def cancelar(id_evento):
        CancelarEventoService().executar(id_evento, session["id_usuario"])
        return "", 204

    @staticmethod
    def comentar(id_evento):
        dados = request.get_json(silent=True) or {}
        comentario = ComentarEventoService().executar(
            id_evento, session["id_usuario"], dados.get("texto")
        )
        return jsonify(comment=comentario), 201
