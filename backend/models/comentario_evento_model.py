from extensions import db
from models.crud import CrudMixin
from models.usuario_model import Usuario


class ComentarioEvento(CrudMixin, db.Model):
    __tablename__ = "comentario_evento"

    idComentario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    texto = db.Column(db.Text, nullable=False)
    dataEnvio = db.Column(db.DateTime, nullable=False, default=db.func.now())
    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)
    idEvento = db.Column(db.Integer, db.ForeignKey("evento.idEvento"), nullable=False)

    @classmethod
    def listar_por_usuario(cls, id_usuario):
        return cls.query.filter_by(idUsuario=id_usuario).all()

    def to_dict(self):
        autor = db.session.get(Usuario, self.idUsuario)
        return {"idComentario": self.idComentario, "texto": self.texto,
                "dataEnvio": self.dataEnvio.isoformat() if self.dataEnvio else None,
                "nomeUsuario": autor.nome if autor else "Usuário"}
