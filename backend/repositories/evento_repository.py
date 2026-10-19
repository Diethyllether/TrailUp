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

    def detalhes_em_lote(self, ids_evento):
        if not ids_evento:
            return {}
        vinculos = db.session.query(EventoTrilha).filter(EventoTrilha.idEvento.in_(ids_evento)).all()
        participantes = (db.session.query(ParticipanteEvento.idEvento, Usuario.nome)
            .join(Usuario, Usuario.idUsuario == ParticipanteEvento.idUsuario)
            .filter(ParticipanteEvento.idEvento.in_(ids_evento)).all())
        comentarios = (db.session.query(ComentarioEvento, Usuario.nome)
            .join(Usuario, Usuario.idUsuario == ComentarioEvento.idUsuario)
            .filter(ComentarioEvento.idEvento.in_(ids_evento))
            .order_by(ComentarioEvento.dataEnvio.asc()).all())
        criadores = (db.session.query(Evento.idEvento, Usuario.nome)
            .join(Usuario, Usuario.idUsuario == Evento.idCriador)
            .filter(Evento.idEvento.in_(ids_evento)).all())
        dados = {id_evento: {"trilhasIds": [], "participantes": [], "participantesAtuais": 0,
            "comentarios": [], "nomeCriador": None} for id_evento in ids_evento}
        for vinculo in vinculos:
            dados[vinculo.idEvento]["trilhasIds"].append(vinculo.idTrilha)
        for id_evento, nome in participantes:
            dados[id_evento]["participantes"].append(nome)
            dados[id_evento]["participantesAtuais"] += 1
        for comentario, nome in comentarios:
            dados[comentario.idEvento]["comentarios"].append({
                "idComentario": comentario.idComentario, "texto": comentario.texto,
                "dataEnvio": comentario.dataEnvio.isoformat() if comentario.dataEnvio else None,
                "nomeUsuario": nome,
            })
        for id_evento, nome in criadores:
            dados[id_evento]["nomeCriador"] = nome
        return dados
