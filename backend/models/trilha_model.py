from extensions import db

class Trilha(db.Model):
    __tablename__ = "trilha"

    idTrilha = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    localizacao = db.Column(db.String(200), nullable=True)
    distancia = db.Column(db.Float, nullable=True)
    duracao = db.Column(db.Float, nullable=True)
    dificuldade = db.Column(db.String(50), nullable=True)
    descricao = db.Column(db.Text, nullable=True)
    imagemUrl = db.Column(db.String(255), nullable=True)
    tempoEstimadoMin = db.Column(db.Float, nullable=True)

    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def atualizar(self):
        db.session.commit()
        return self

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def listar_todos(cls):
        return cls.query.all()

    @classmethod
    def buscar_por_id(cls, id_trilha):
        return cls.query.get(id_trilha)

    def to_dict(self):
        return {
            "idTrilha": self.idTrilha,
            "nome": self.nome,
            "localizacao": self.localizacao,
            "distancia": self.distancia,
            "duracao": self.duracao,
            "dificuldade": self.dificuldade,
            "descricao": self.descricao,
            "imagemUrl": self.imagemUrl,
            "tempoEstimadoMin": self.tempoEstimadoMin,
        }
