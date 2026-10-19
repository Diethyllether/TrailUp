"""Consultas agregadas de histórico pelo procedimento do MySQL."""

from sqlalchemy import text

from extensions import db


class HistoricoRepository:
    def listar_por_usuario(self, id_usuario):
        resultado = db.session.execute(
            text("CALL sp_historico_usuario(:id_usuario)"), {"id_usuario": id_usuario}
        )
        try:
            return [dict(linha) for linha in resultado.mappings().all()]
        finally:
            resultado.close()
