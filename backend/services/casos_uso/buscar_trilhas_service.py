from models.trilha_model import Trilha
from repositories.trilha_repository import TrilhaRepository
from utils.normalizacao import normalizar_dificuldade

class BuscarTrilhasService:
    def __init__(self, repository=None):
        self.repository = repository or TrilhaRepository()

    def executar(self, nome=None, localizacao=None, dificuldade=None, busca=None):
        if nome or localizacao or dificuldade or busca:
            return self.repository.buscar(
                nome=nome,
                localizacao=localizacao,
                dificuldade=normalizar_dificuldade(dificuldade),
                busca=busca,
            )
        return Trilha.listar_todos()
