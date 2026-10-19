from models.favorito_model import Favorito
from utils.excecoes import RecursoNaoEncontrado


class RemoverFavoritoService:
    def __init__(self, modelo_favorito=None):
        self.modelo_favorito = modelo_favorito or Favorito

    def executar(self, id_usuario, id_trilha):
        favorito = self.modelo_favorito.buscar(id_usuario, id_trilha)
        if favorito is None:
            raise RecursoNaoEncontrado("trilha não está nos favoritos deste usuário")
        favorito.deletar()
        return {"removido": True}
