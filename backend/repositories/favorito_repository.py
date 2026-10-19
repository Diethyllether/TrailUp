"""Leitura dos favoritos pelo procedimento com dados dos cards."""

from sqlalchemy import text

from extensions import db


class FavoritoRepository:
    def listar_por_usuario(self, id_usuario):
        resultado = db.session.execute(
            text("CALL sp_favoritos_usuario(:id_usuario)"), {"id_usuario": id_usuario}
        )
        try:
            return [dict(linha) for linha in resultado.mappings().all()]
        finally:
            resultado.close()
