"""Consultas agregadas de relatórios executadas por procedures MySQL."""

from sqlalchemy import text

from extensions import db


class RelatorioRepository:
    @staticmethod
    def _executar(call_sql, parametros):
        resultado = db.session.execute(text(call_sql), parametros)
        try:
            return [dict(linha) for linha in resultado.mappings().all()]
        finally:
            resultado.close()

    def trilhas_ordenadas(self, dificuldade=None, localizacao=None, ordem="nota"):
        return self._executar(
            "CALL sp_trilhas_por_dificuldade(:dificuldade, :localizacao, :ordem)",
            {"dificuldade": dificuldade, "localizacao": localizacao, "ordem": ordem},
        )

    def favoritos_usuario(self, id_usuario):
        return self._executar(
            "CALL sp_favoritos_usuario(:id_usuario)", {"id_usuario": id_usuario}
        )

    def resumo_usuario(self, id_usuario):
        linhas = self._executar(
            "CALL sp_resumo_usuario(:id_usuario)", {"id_usuario": id_usuario}
        )
        return linhas[0] if linhas else None

    def ranking_usuarios(self, limite=10):
        return self._executar(
            "CALL sp_ranking_usuarios(:limite)", {"limite": limite}
        )

    def eventos_ativos(self):
        return self._executar("CALL sp_eventos_ativos()", {})
