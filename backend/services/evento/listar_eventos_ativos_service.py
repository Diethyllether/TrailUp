from repositories.evento_repository import EventoRepository
from models.participante_evento_model import ParticipanteEvento
from models.trilha_model import Trilha


class ListarEventosAtivosService:
    def __init__(self, repository=None):
        self.repository = repository or EventoRepository()

    def executar(self, id_usuario=None):
        eventos = self.repository.listar_ativos()
        detalhes = self.repository.detalhes_em_lote([item.idEvento for item in eventos])
        itens = [
            {**evento.to_dict(), **detalhes.get(evento.idEvento, {})}
            for evento in eventos
        ]
        participantes = [
            evento.idEvento for evento in eventos
            if id_usuario and ParticipanteEvento.buscar(id_usuario, evento.idEvento)
        ]
        return {
            "items": itens,
            "participating": participantes,
            "trails": [trilha.to_dict() for trilha in Trilha.listar_todos()],
        }
