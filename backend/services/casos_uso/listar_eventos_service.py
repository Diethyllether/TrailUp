from repositories.evento_repository import EventoRepository
from repositories.usuario_repository import UsuarioRepository

class ListarEventosService:
    def __init__(self, repository=None, usuario_repository=None):
        self.repository = repository or EventoRepository()
        self.usuario_repository = usuario_repository or UsuarioRepository()

    def executar(self, apenas_mapa=False):
        if apenas_mapa:
            return self.repository.listar_ativos()
        return self.repository.listar_todos()

    def serializar(self, evento):
        dados = evento.to_dict()
        vinculos = self.repository.listar_trilhas_do_evento(evento.idEvento)
        dados["trilhasIds"] = [v.idTrilha for v in vinculos]
        dados["participantesAtuais"] = self.repository.contar_participantes(evento.idEvento)
        criador = self.usuario_repository.buscar_por_id(evento.idCriador)
        dados["nomeCriador"] = criador.nome if criador else None
        return dados
