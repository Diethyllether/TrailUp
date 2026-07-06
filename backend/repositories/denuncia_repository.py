from models.denuncia_model import Denuncia
from repositories.base_repository import BaseRepository

class DenunciaRepository(BaseRepository):
    model = Denuncia

    def listar_por_evento(self, id_evento):
        return Denuncia.query.filter_by(idEvento=id_evento).all()
