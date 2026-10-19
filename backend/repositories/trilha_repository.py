"""Consultas especializadas de trilhas executadas por procedures MySQL."""

from sqlalchemy import text

from extensions import db
from models.avaliacao_model import Avaliacao
from models.trilha_model import Trilha


def _executar(call_sql, parametros):
    resultado = db.session.execute(text(call_sql), parametros)
    try:
        return [dict(linha) for linha in resultado.mappings().all()]
    finally:
        resultado.close()


def _trilha_da_linha(linha):
    campos = {
        "idTrilha", "nome", "localizacao", "distancia", "duracao", "dificuldade",
        "descricao", "imagemUrl", "tempoEstimadoMin",
    }
    return Trilha(**{chave: valor for chave, valor in linha.items() if chave in campos})


class TrilhaRepository:
    """Executa consultas de busca, filtro, avaliação e proximidade no MySQL."""

    model = Trilha

    def buscar(self, nome=None, localizacao=None, dificuldade=None, busca=None):
        termo = busca or nome or localizacao
        linhas = _executar(
            "CALL sp_buscar_trilhas(:termo, :dificuldade)",
            {"termo": termo, "dificuldade": dificuldade},
        )
        return [_trilha_da_linha(linha) for linha in linhas]

    def listar_ordenadas(self, ordenacao=None, distancia_max=None, duracao_max=None, nota_min=None):
        linhas = _executar(
            "CALL sp_filtrar_trilhas(:distancia_max, :duracao_max, :nota_min, :ordem)",
            {
                "distancia_max": distancia_max,
                "duracao_max": duracao_max,
                "nota_min": nota_min,
                "ordem": ordenacao,
            },
        )
        return [_trilha_da_linha(linha) for linha in linhas]

    def medias_avaliacao(self):
        linhas = _executar("CALL sp_medias_trilhas()", {})
        return {
            linha["idTrilha"]: (linha["media"], linha["quantidade"])
            for linha in linhas
        }

    def avaliacoes_com_autores(self, id_trilha):
        linhas = _executar(
            "CALL sp_avaliacoes_trilha(:id_trilha)", {"id_trilha": id_trilha}
        )
        campos = {"idAvaliacao", "nota", "comentario", "data", "idUsuario", "idTrilha"}
        return [
            (Avaliacao(**{chave: valor for chave, valor in linha.items() if chave in campos}),
             linha["nomeUsuario"])
            for linha in linhas
        ]

    def trilhas_proximas(self, latitude, longitude, limite=6):
        return _executar(
            "CALL sp_trilhas_proximas(:latitude, :longitude, :limite)",
            {"latitude": latitude, "longitude": longitude, "limite": limite},
        )
