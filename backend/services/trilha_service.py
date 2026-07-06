import unicodedata

from models.trilha_model import Trilha
from repositories.trilha_repository import TrilhaRepository

VELOCIDADE_POR_DIFICULDADE = {
    "FACIL": 4.0,
    "MODERADA": 3.0,
    "DIFICIL": 2.0,
}

def _normalizar_dificuldade(valor):
    """Aceita variações vindas do app (ex: 'Fácil', 'Moderado', 'difícil')
    e normaliza para o código canônico salvo no banco (FACIL/MODERADA/DIFICIL).
    """
    if not valor:
        return valor
    sem_acento = unicodedata.normalize("NFKD", valor).encode("ascii", "ignore").decode()
    codigo = sem_acento.strip().upper()
    if codigo in ("MODERADO", "MODERADA"):
        return "MODERADA"
    if codigo in VELOCIDADE_POR_DIFICULDADE:
        return codigo
    return valor

class TrilhaService:
    def __init__(self):
        self.repository = TrilhaRepository()

    @staticmethod
    def calcular_tempo_estimado_min(distancia_km, dificuldade):
        if not distancia_km:
            return None
        velocidade = VELOCIDADE_POR_DIFICULDADE.get((dificuldade or "").upper(), 3.0)
        horas = distancia_km / velocidade
        return round(horas * 60, 1)

    def listar_todos(self):
        return self.repository.listar_todos()

    def buscar(self, nome=None, localizacao=None, dificuldade=None, busca=None):
        return self.repository.buscar(
            nome=nome,
            localizacao=localizacao,
            dificuldade=_normalizar_dificuldade(dificuldade),
            busca=busca,
        )

    def buscar_por_id(self, id_trilha):
        trilha = self.repository.buscar_por_id(id_trilha)
        if not trilha:
            raise ValueError("trilha não encontrada")
        return trilha

    def criar(self, dados):
        if not dados.get("nome"):
            raise ValueError("nome da trilha é obrigatório")

        tempo_estimado = self.calcular_tempo_estimado_min(
            dados.get("distancia"), dados.get("dificuldade")
        )

        trilha = Trilha(
            nome=dados["nome"],
            localizacao=dados.get("localizacao"),
            distancia=dados.get("distancia"),
            duracao=dados.get("duracao"),
            dificuldade=_normalizar_dificuldade(dados.get("dificuldade")),
            descricao=dados.get("descricao"),
            imagemUrl=dados.get("imagemUrl"),
            tempoEstimadoMin=tempo_estimado,
        )
        self.repository.criar(trilha)
        return trilha

    def atualizar(self, id_trilha, dados):
        trilha = self.buscar_por_id(id_trilha)

        for campo in ("nome", "localizacao", "distancia", "duracao", "dificuldade", "descricao", "imagemUrl"):
            if campo in dados:
                valor = dados[campo]
                if campo == "dificuldade":
                    valor = _normalizar_dificuldade(valor)
                setattr(trilha, campo, valor)

        trilha.tempoEstimadoMin = self.calcular_tempo_estimado_min(
            trilha.distancia, trilha.dificuldade
        )

        self.repository.atualizar()
        return trilha

    def deletar(self, id_trilha):
        trilha = self.buscar_por_id(id_trilha)
        self.repository.deletar(trilha)
