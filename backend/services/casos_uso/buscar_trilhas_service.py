import unicodedata

from models.trilha_model import Trilha
from repositories.trilha_repository import TrilhaRepository

def _normalizar_dificuldade(valor):
    if not valor:
        return valor
    sem_acento = unicodedata.normalize("NFKD", valor).encode("ascii", "ignore").decode()
    codigo = sem_acento.strip().upper()
    if codigo in ("MODERADO", "MODERADA"):
        return "MODERADA"
    if codigo in ("FACIL", "DIFICIL"):
        return codigo
    return valor

class BuscarTrilhasService:
    def __init__(self):
        self.repository = TrilhaRepository()

    def executar(self, nome=None, localizacao=None, dificuldade=None, busca=None):
        if nome or localizacao or dificuldade or busca:
            return self.repository.buscar(
                nome=nome,
                localizacao=localizacao,
                dificuldade=_normalizar_dificuldade(dificuldade),
                busca=busca,
            )
        return Trilha.listar_todos()
