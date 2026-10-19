from models.favorito_model import Favorito

class RemoverFavoritoService:
    def __init__(self, repository=None):
        self.repository = repository

    def executar(self, id_usuario, id_trilha):
        favorito = Favorito.query.filter_by(idUsuario=id_usuario, idTrilha=id_trilha).first()
        if not favorito:
            raise ValueError("trilha não está nos favoritos deste usuário")
        favorito.deletar()
