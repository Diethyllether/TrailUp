from extensions import db
from models.evento_model import Evento
from models.evento_trilha_model import EventoTrilha
from models.participante_evento_model import ParticipanteEvento
from models.comentario_evento_model import ComentarioEvento
from models.usuario_model import Usuario


class EventoRepository:
    """Acesso especializado a vínculos, participantes e consultas de eventos."""

    model = Evento

    def listar_ativos(self):
        return Evento.query.filter(
            Evento.latitude.isnot(None), Evento.longitude.isnot(None)
        ).all()

    def listar_trilhas_do_evento(self, id_evento):
        return EventoTrilha.query.filter_by(idEvento=id_evento).all()

    def listar_por_trilha(self, id_trilha):
        return (
            Evento.query.join(EventoTrilha, EventoTrilha.idEvento == Evento.idEvento)
            .filter(EventoTrilha.idTrilha == id_trilha)
            .all()
        )

    def listar_por_usuario(self, id_usuario):
        """Expedições das quais o usuário é participante."""
        return (
            Evento.query.join(
                ParticipanteEvento,
                ParticipanteEvento.idEvento == Evento.idEvento,
            )
            .filter(ParticipanteEvento.idUsuario == id_usuario)
            .order_by(Evento.data.desc(), Evento.horarioSaida.desc())
            .all()
        )

    def listar_participantes(self, id_evento):
        return ParticipanteEvento.query.filter_by(idEvento=id_evento).all()

    def listar_comentarios(self, id_evento):
        return (db.session.query(ComentarioEvento, Usuario.nome)
                .join(Usuario, Usuario.idUsuario == ComentarioEvento.idUsuario)
                .filter(ComentarioEvento.idEvento == id_evento)
                .order_by(ComentarioEvento.dataEnvio.asc()).all())

    def contar_participantes(self, id_evento):
        return ParticipanteEvento.query.filter_by(idEvento=id_evento).count()
