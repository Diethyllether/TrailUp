from models.evento_model import Evento
from models.participante_evento_model import ParticipanteEvento
from repositories.evento_repository import EventoRepository
from utils.excecoes import ConflitoDeDados, RecursoNaoEncontrado


class ParticiparEventoService:
    def __init__(self, repository=None, modelo_evento=None, modelo_participante=None):
        self.repository = repository or EventoRepository()
        self.modelo_evento = modelo_evento or Evento
        self.modelo_participante = modelo_participante or ParticipanteEvento

    def executar(self, id_evento, id_usuario):
        evento = self.modelo_evento.buscar_por_id(id_evento)
        if evento is None:
            raise RecursoNaoEncontrado("evento não encontrado")
        if self.modelo_participante.buscar(id_usuario, id_evento):
            return {"participating": True}
        if evento.vagas is not None and self.repository.contar_participantes(id_evento) >= evento.vagas:
            raise ConflitoDeDados("sala sem vagas disponíveis")
        self.modelo_participante(idUsuario=id_usuario, idEvento=id_evento).salvar()
        return {"participating": True}
