from models.evento_model import Evento, ComentarioEvento
from repositories.evento_repository import EventoRepository
from repositories.checkpoint_repository import CheckpointRepository
from repositories.usuario_repository import UsuarioRepository
from services.casos_uso import ListarEventosService, ParticiparEventoService


class EventoService:
    """Facade de eventos; listagem e participação possuem casos de uso próprios."""

    def __init__(self, repository=None, usuario_repository=None, checkpoint_repository=None):
        self.repository = repository or EventoRepository()
        self.usuario_repository = usuario_repository or UsuarioRepository()
        self.checkpoint_repository = checkpoint_repository or CheckpointRepository()
        self.listar_eventos_service = ListarEventosService(
            self.repository, self.usuario_repository
        )
        self.participar_evento_service = ParticiparEventoService(self.repository)

    def listar_todos(self):
        return self.listar_eventos_service.executar()

    def listar_ativos_no_mapa(self):
        return self.listar_eventos_service.executar(apenas_mapa=True)

    def listar_por_trilha(self, id_trilha):
        return self.repository.listar_por_trilha(id_trilha)

    def listar_por_usuario(self, id_usuario):
        return self.repository.listar_por_usuario(id_usuario)

    def usuario_participa(self, id_usuario, id_evento):
        return self.repository.buscar_participante(id_usuario, id_evento) is not None

    def to_dict_completo(self, evento):
        dados = evento.to_dict()
        vinculos = self.repository.listar_trilhas_do_evento(evento.idEvento)
        dados["trilhasIds"] = [v.idTrilha for v in vinculos]
        dados["participantesAtuais"] = self.repository.contar_participantes(evento.idEvento)
        dados["participantes"] = self.listar_participantes(evento.idEvento)
        dados["comentarios"] = self.listar_comentarios(evento.idEvento)
        criador = self.usuario_repository.buscar_por_id(evento.idCriador)
        dados["nomeCriador"] = criador.nome if criador else None
        return dados

    def buscar_por_id(self, id_evento):
        evento = self.repository.buscar_por_id(id_evento)
        if not evento:
            raise ValueError("evento não encontrado")
        return evento

    def _coordenadas_da_trilha(self, ids_trilha):
        """Usa o primeiro checkpoint GPS válido da primeira trilha vinculada."""
        for id_trilha in ids_trilha or []:
            checkpoint = self.checkpoint_repository.primeiro_valido_por_trilha(id_trilha)
            if checkpoint:
                return float(checkpoint.latitude), float(checkpoint.longitude)
        return None, None

    def criar(self, id_criador, dados):
        if not dados.get("titulo") or not dados.get("tipo"):
            raise ValueError("titulo e tipo são obrigatórios")
        if dados["tipo"] not in ("INDIVIDUAL", "GRUPO"):
            raise ValueError("tipo deve ser INDIVIDUAL ou GRUPO")

        latitude = dados.get("latitude")
        longitude = dados.get("longitude")
        ids_trilha = dados.get("trilhas", [])

        # Se o cliente não informou uma posição própria para a expedição,
        # ancora o evento na rota real da trilha vinculada para que apareça
        # corretamente no mapa.
        if latitude is None or longitude is None:
            latitude_trilha, longitude_trilha = self._coordenadas_da_trilha(ids_trilha)
            if latitude is None:
                latitude = latitude_trilha
            if longitude is None:
                longitude = longitude_trilha

        evento = Evento(
            titulo=dados["titulo"],
            descricao=dados.get("descricao"),
            data=dados.get("data"),
            horarioSaida=dados.get("horarioSaida"),
            imediata=bool(dados.get("imediata", False)),
            vagas=dados.get("vagas"),
            tipo=dados["tipo"],
            latitude=latitude,
            longitude=longitude,
            idCriador=id_criador,
        )
        self.repository.criar(evento)

        for id_trilha in ids_trilha:
            self.repository.vincular_trilha(evento.idEvento, id_trilha)

        self.repository.adicionar_participante(id_criador, evento.idEvento)
        return evento

    def atualizar(self, id_evento, id_usuario, dados):
        evento = self.buscar_por_id(id_evento)
        if evento.idCriador != id_usuario:
            raise PermissionError("apenas o criador pode editar a sala")

        for campo in (
            "titulo", "descricao", "data", "horarioSaida", "imediata",
            "vagas", "tipo", "latitude", "longitude",
        ):
            if campo in dados:
                setattr(evento, campo, dados[campo])

        self.repository.atualizar()
        return evento

    def deletar(self, id_evento, id_usuario):
        evento = self.buscar_por_id(id_evento)
        if evento.idCriador != id_usuario:
            raise PermissionError("apenas o criador pode remover a sala")
        self.repository.deletar(evento)

    def entrar(self, id_evento, id_usuario):
        return self.participar_evento_service.executar(id_evento, id_usuario)

    def sair(self, id_evento, id_usuario):
        return self.repository.remover_participante(id_usuario, id_evento)

    def listar_participantes(self, id_evento):
        evento = self.buscar_por_id(id_evento)
        return [u.nome for p in self.repository.listar_participantes(evento.idEvento)
                if (u := self.usuario_repository.buscar_por_id(p.idUsuario))]

    def listar_comentarios(self, id_evento):
        return [{**comentario.to_dict(), "nomeUsuario": nome}
                for comentario, nome in self.repository.listar_comentarios(id_evento)]

    def comentar(self, id_evento, id_usuario, texto):
        if not self.usuario_participa(id_usuario, id_evento):
            raise PermissionError("apenas participantes confirmados podem comentar")
        texto = (texto or "").strip()
        if not texto or len(texto) > 2000:
            raise ValueError("comentário deve ter entre 1 e 2000 caracteres")
        return self.repository.criar_comentario(ComentarioEvento(texto=texto, idUsuario=id_usuario, idEvento=id_evento))

    def listar_trilhas(self, id_evento):
        return self.repository.listar_trilhas_do_evento(id_evento)
