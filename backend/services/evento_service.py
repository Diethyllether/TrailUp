from models.evento_model import Evento
from repositories.evento_repository import EventoRepository
from repositories.usuario_repository import UsuarioRepository

class EventoService:
    def __init__(self):
        self.repository = EventoRepository()
        self.usuario_repository = UsuarioRepository()

    def listar_todos(self):
        return self.repository.listar_todos()

    def listar_ativos_no_mapa(self):
        return self.repository.listar_ativos()

    def listar_por_trilha(self, id_trilha):
        return self.repository.listar_por_trilha(id_trilha)

    def to_dict_completo(self, evento):
        """Serializa o evento já incluindo os campos agregados que o app
        Flutter espera (vindos das tabelas de junção evento_trilha /
        participante_evento e de um join simples com usuario)."""
        dados = evento.to_dict()
        vinculos = self.repository.listar_trilhas_do_evento(evento.idEvento)
        dados["trilhasIds"] = [v.idTrilha for v in vinculos]
        dados["participantesAtuais"] = self.repository.contar_participantes(evento.idEvento)
        criador = self.usuario_repository.buscar_por_id(evento.idCriador)
        dados["nomeCriador"] = criador.nome if criador else None
        return dados

    def buscar_por_id(self, id_evento):
        evento = self.repository.buscar_por_id(id_evento)
        if not evento:
            raise ValueError("evento não encontrado")
        return evento

    def criar(self, id_criador, dados):
        if not dados.get("titulo") or not dados.get("tipo"):
            raise ValueError("titulo e tipo são obrigatórios")
        if dados["tipo"] not in ("INDIVIDUAL", "GRUPO"):
            raise ValueError("tipo deve ser INDIVIDUAL ou GRUPO")

        evento = Evento(
            titulo=dados["titulo"],
            descricao=dados.get("descricao"),
            data=dados.get("data"),
            horarioSaida=dados.get("horarioSaida"),
            imediata=bool(dados.get("imediata", False)),
            vagas=dados.get("vagas"),
            tipo=dados["tipo"],
            latitude=dados.get("latitude"),
            longitude=dados.get("longitude"),
            idCriador=id_criador,
        )
        self.repository.criar(evento)

        for id_trilha in dados.get("trilhas", []):
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
        evento = self.buscar_por_id(id_evento)
        if evento.vagas is not None:
            ocupadas = self.repository.contar_participantes(id_evento)
            if ocupadas >= evento.vagas:
                raise ValueError("sala sem vagas disponíveis")
        return self.repository.adicionar_participante(id_usuario, id_evento)

    def sair(self, id_evento, id_usuario):
        return self.repository.remover_participante(id_usuario, id_evento)

    def listar_participantes(self, id_evento):
        return self.repository.listar_participantes(id_evento)

    def listar_trilhas(self, id_evento):
        return self.repository.listar_trilhas_do_evento(id_evento)
