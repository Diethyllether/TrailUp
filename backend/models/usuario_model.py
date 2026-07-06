from datetime import date
from extensions import db

class Usuario(db.Model):
    __tablename__ = "usuario"

    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    fotoPerfil = db.Column(db.String(255), nullable=True)
    dataCadastro = db.Column(db.Date, default=date.today)

    def to_dict(self, include_senha=False):
        data = {
            "idUsuario": self.idUsuario,
            "nome": self.nome,
            "email": self.email,
            "fotoPerfil": self.fotoPerfil,
            "dataCadastro": self.dataCadastro.isoformat() if self.dataCadastro else None,
        }
        if include_senha:
            data["senha"] = self.senha
        return data
