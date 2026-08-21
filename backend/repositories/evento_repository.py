from extensions import db
from models.evento_model import Evento, EventoTrilha, ParticipanteEvento

class EventoRepository:
    """Acesso especializado a vínculos, participantes e consultas de eventos."""

    def listar_ativos(self):
        return Evento.query.filter(
            Evento.latitude.isnot(None), Evento.longitude.isnot(None)
        ).all()

    def vincular_trilha(self, id_evento, id_trilha):
        vinculo = EventoTrilha(idEvento=id_evento, idTrilha=id_trilha)
        db.session.add(vinculo)
        db.session.commit()
        return vinculo

    def listar_trilhas_do_evento(self, id_evento):
        return EventoTrilha.query.filter_by(idEvento=id_evento).all()

    def listar_por_trilha(self, id_trilha):
        return (
            Evento.query.join(EventoTrilha, EventoTrilha.idEvento == Evento.idEvento)
            .filter(EventoTrilha.idTrilha == id_trilha)
            .all()
        )

    def buscar_participante(self, id_usuario, id_evento):
        return ParticipanteEvento.query.filter_by(
            idUsuario=id_usuario, idEvento=id_evento
        ).first()

    def adicionar_participante(self, id_usuario, id_evento):
        participante = ParticipanteEvento(idUsuario=id_usuario, idEvento=id_evento)
        db.session.add(participante)
        db.session.commit()
        return participante

    def remover_participante(self, id_usuario, id_evento):
        participante = self.buscar_participante(id_usuario, id_evento)
        if participante:
            db.session.delete(participante)
            db.session.commit()
        return participante

    def listar_participantes(self, id_evento):
        return ParticipanteEvento.query.filter_by(idEvento=id_evento).all()

    def contar_participantes(self, id_evento):
        return ParticipanteEvento.query.filter_by(idEvento=id_evento).count()
