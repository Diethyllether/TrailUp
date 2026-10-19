from models.evento_model import Evento
from utils.excecoes import PermissaoNegada, RecursoNaoEncontrado


class CancelarEventoService:
    def __init__(self, modelo_evento=None):
        self.modelo_evento = modelo_evento or Evento

    def executar(self, id_evento, id_usuario):
        evento = self.modelo_evento.buscar_por_id(id_evento)
        if evento is None:
            raise RecursoNaoEncontrado("evento não encontrado")
        if evento.idCriador != id_usuario:
            raise PermissaoNegada("apenas o criador pode cancelar a expedição")
        evento.deletar()
        return {"cancelado": True}
