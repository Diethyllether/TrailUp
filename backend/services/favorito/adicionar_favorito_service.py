from models.favorito_model import Favorito
from models.trilha_model import Trilha
from utils.excecoes import RecursoNaoEncontrado


class AdicionarFavoritoService:
    def __init__(self, modelo_favorito=None, modelo_trilha=None):
        self.modelo_favorito = modelo_favorito or Favorito
        self.modelo_trilha = modelo_trilha or Trilha

    def executar(self, id_usuario, id_trilha):
        if not self.modelo_trilha.buscar_por_id(id_trilha):
            raise RecursoNaoEncontrado("trilha não encontrada")
        favorito = self.modelo_favorito.buscar(id_usuario, id_trilha)
        if favorito is None:
            favorito = self.modelo_favorito(
                idUsuario=id_usuario, idTrilha=id_trilha
            ).salvar()
        return favorito.to_dict()
