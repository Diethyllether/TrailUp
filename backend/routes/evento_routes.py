from flask import Blueprint

from controllers.evento_controller import EventoController
from utils.decorators import login_obrigatorio

evento_bp = Blueprint("eventos", __name__)


@evento_bp.get("/events")
def listar_eventos():
    return EventoController.listar()


@evento_bp.post("/events")
@login_obrigatorio
def criar_evento():
    return EventoController.criar()


@evento_bp.post("/events/<int:id_evento>/participation")
@login_obrigatorio
def participar_evento(id_evento):
    return EventoController.participar(id_evento)


@evento_bp.delete("/events/<int:id_evento>/participation")
@login_obrigatorio
def sair_evento(id_evento):
    return EventoController.sair(id_evento)


@evento_bp.put("/events/<int:id_evento>")
@login_obrigatorio
def atualizar_evento(id_evento):
    return EventoController.atualizar(id_evento)


@evento_bp.delete("/events/<int:id_evento>")
@login_obrigatorio
def cancelar_evento(id_evento):
    return EventoController.cancelar(id_evento)


@evento_bp.post("/events/<int:id_evento>/comments")
@login_obrigatorio
def comentar_evento(id_evento):
    return EventoController.comentar(id_evento)
