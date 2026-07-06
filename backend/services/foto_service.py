from models.foto_model import Foto
from repositories.foto_repository import FotoRepository

class FotoService:
    def __init__(self):
        self.repository = FotoRepository()

    def listar_por_trilha(self, id_trilha):
        return self.repository.listar_por_trilha(id_trilha)

    def buscar_por_id(self, id_foto):
        foto = self.repository.buscar_por_id(id_foto)
        if not foto:
            raise ValueError("foto não encontrada")
        return foto

    def criar(self, dados):
        if not dados.get("idTrilha") or not dados.get("url"):
            raise ValueError("idTrilha e url são obrigatórios")

        foto = Foto(url=dados["url"], legenda=dados.get("legenda"), idTrilha=dados["idTrilha"])
        self.repository.criar(foto)
        return foto

    def deletar(self, id_foto):
        foto = self.buscar_por_id(id_foto)
        self.repository.deletar(foto)
