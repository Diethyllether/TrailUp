from repositories.evento_repository import EventoRepository

class ParticiparEventoService:
    def __init__(self, repository=None):
        self.repository = repository or EventoRepository()

    def executar(self, id_evento, id_usuario):
        evento = self.repository.buscar_por_id(id_evento)
        if not evento:
            raise ValueError("evento não encontrado")

        ja_participa = self.repository.buscar_participante(id_usuario, id_evento)
        if ja_participa:
            return ja_participa

        if evento.vagas is not None:
            ocupadas = self.repository.contar_participantes(id_evento)
            if ocupadas >= evento.vagas:
                raise ValueError("sala sem vagas disponíveis")

        return self.repository.adicionar_participante(id_usuario, id_evento)
