from models.evento_model import Evento
from models.usuario_model import Usuario
from repositories.evento_repository import EventoRepository

class ListarEventosService:
    def __init__(self):
        self.repository = EventoRepository()

    def executar(self, apenas_mapa=False):
        if apenas_mapa:
            return self.repository.listar_ativos()
        return Evento.listar_todos()

    def serializar(self, evento):
        dados = evento.to_dict()
        vinculos = self.repository.listar_trilhas_do_evento(evento.idEvento)
        dados["trilhasIds"] = [v.idTrilha for v in vinculos]
        dados["participantesAtuais"] = self.repository.contar_participantes(evento.idEvento)
        criador = Usuario.buscar_por_id(evento.idCriador)
        dados["nomeCriador"] = criador.nome if criador else None
        return dados
