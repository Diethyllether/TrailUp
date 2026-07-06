from extensions import db

class Evento(db.Model):
    __tablename__ = "evento"

    idEvento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data = db.Column(db.Date, nullable=True)
    horarioSaida = db.Column(db.DateTime, nullable=True)
    imediata = db.Column(db.Boolean, default=False)
    vagas = db.Column(db.Integer, nullable=True)
    tipo = db.Column(db.Enum("INDIVIDUAL", "GRUPO", name="tipo_evento"), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    idCriador = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)

    def to_dict(self):
        return {
            "idEvento": self.idEvento,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "data": self.data.isoformat() if self.data else None,
            "horarioSaida": self.horarioSaida.isoformat() if self.horarioSaida else None,
            "imediata": self.imediata,
            "vagas": self.vagas,
            "tipo": self.tipo,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "idCriador": self.idCriador,
        }

class EventoTrilha(db.Model):
    __tablename__ = "evento_trilha"

    idEvento = db.Column(db.Integer, db.ForeignKey("evento.idEvento"), primary_key=True)
    idTrilha = db.Column(db.Integer, db.ForeignKey("trilha.idTrilha"), primary_key=True)

    def to_dict(self):
        return {"idEvento": self.idEvento, "idTrilha": self.idTrilha}

class ParticipanteEvento(db.Model):
    __tablename__ = "participante_evento"

    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), primary_key=True)
    idEvento = db.Column(db.Integer, db.ForeignKey("evento.idEvento"), primary_key=True)

    def to_dict(self):
        return {"idUsuario": self.idUsuario, "idEvento": self.idEvento}
