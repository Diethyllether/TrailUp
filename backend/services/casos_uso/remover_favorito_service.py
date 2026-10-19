from models.favorito_model import Favorito

class RemoverFavoritoService:
    def __init__(self, repository=None):
        self.repository = repository

    def executar(self, id_usuario, id_trilha):
        favorito = Favorito.buscar(id_usuario, id_trilha)
        if not favorito:
            raise ValueError("trilha não está nos favoritos deste usuário")
        favorito.deletar()
