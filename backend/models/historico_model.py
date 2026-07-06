from extensions import db

class HistoricoTrilha(db.Model):
    __tablename__ = "historicoTrilha"

    idHistorico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dataRealizacao = db.Column(db.Date, nullable=True)
    tempo = db.Column(db.Float, nullable=True)
    avaliacaoPessoal = db.Column(db.Integer, nullable=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)
    idEvento = db.Column(db.Integer, db.ForeignKey("evento.idEvento"), nullable=True)
    idTrilha = db.Column(db.Integer, db.ForeignKey("trilha.idTrilha"), nullable=False)

    def to_dict(self):
        return {
            "idHistorico": self.idHistorico,
            "dataRealizacao": self.dataRealizacao.isoformat() if self.dataRealizacao else None,
            "tempo": self.tempo,
            "avaliacaoPessoal": self.avaliacaoPessoal,
            "idUsuario": self.idUsuario,
            "idEvento": self.idEvento,
            "idTrilha": self.idTrilha,
        }

class RegistroRealizado(db.Model):
    __tablename__ = "registroRealizado"

    idRegistro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    horario = db.Column(db.DateTime, nullable=True)
    observacao = db.Column(db.Text, nullable=True)
    idHistorico = db.Column(db.Integer, db.ForeignKey("historicoTrilha.idHistorico"), nullable=False)

    def to_dict(self):
        return {
            "idRegistro": self.idRegistro,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "horario": self.horario.isoformat() if self.horario else None,
            "observacao": self.observacao,
            "idHistorico": self.idHistorico,
        }

class FotoRegistro(db.Model):
    __tablename__ = "fotoRegistro"

    idFotoRegistro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=True)
    legenda = db.Column(db.String(255), nullable=True)
    idRegistro = db.Column(db.Integer, db.ForeignKey("registroRealizado.idRegistro"), nullable=False)

    def to_dict(self):
        return {
            "idFotoRegistro": self.idFotoRegistro,
            "url": self.url,
            "legenda": self.legenda,
            "idRegistro": self.idRegistro,
        }
