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
    def resumo_usuario(self, id_usuario):
        linhas = _executar(
            "CALL sp_resumo_usuario(:id_usuario)", {"id_usuario": id_usuario}
        )
        return linhas[0] if linhas else None

    def ranking_usuarios(self, limite=10):
        return _executar(
            "CALL sp_ranking_usuarios(:limite)", {"limite": limite}
        )
