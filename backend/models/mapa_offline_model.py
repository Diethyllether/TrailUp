from datetime import date
from extensions import db

class MapaOffline(db.Model):
    __tablename__ = "mapaOffline"

    idMapa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    arquivoUrl = db.Column(db.String(255), nullable=True)
    tamanhoArquivo = db.Column(db.Float, nullable=True)
    dataDownload = db.Column(db.Date, default=date.today)
    idTrilha = db.Column(db.Integer, db.ForeignKey("trilha.idTrilha"), nullable=False)

    def to_dict(self):
        return {
            "idMapa": self.idMapa,
            "arquivoUrl": self.arquivoUrl,
            "tamanhoArquivo": self.tamanhoArquivo,
            "dataDownload": self.dataDownload.isoformat() if self.dataDownload else None,
            "idTrilha": self.idTrilha,
        }
