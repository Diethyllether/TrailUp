"""Consultas agregadas de relatórios executadas por procedures MySQL."""

from sqlalchemy import text

from extensions import db


def _executar(call_sql, parametros):
    resultado = db.session.execute(text(call_sql), parametros)
    try:
        return [dict(linha) for linha in resultado.mappings().all()]
    finally:
        resultado.close()


class RelatorioRepository:
    def trilhas_ordenadas(self, dificuldade=None, localizacao=None, ordem="nota"):
        return _executar(
            "CALL sp_filtrar_trilhas(:distancia_max, :duracao_max, :nota_min, :ordem)",
            {"distancia_max": None, "duracao_max": None, "nota_min": None, "ordem": ordem},
        )

    def favoritos_usuario(self, id_usuario):
        return _executar(
            "CALL sp_favoritos_usuario(:id_usuario)", {"id_usuario": id_usuario}
        )

    def resumo_usuario(self, id_usuario):
        linhas = _executar(
            "CALL sp_resumo_usuario(:id_usuario)", {"id_usuario": id_usuario}
        )
        return linhas[0] if linhas else None

    def ranking_usuarios(self, limite=10):
        return _executar(
            "CALL sp_ranking_usuarios(:limite)", {"limite": limite}
        )

    def eventos_ativos(self):
        return _executar("CALL sp_eventos_ativos()", {})
