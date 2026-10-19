"""Consultas do checklist persistido por procedures MySQL."""

from sqlalchemy import text

from extensions import db


class ChecklistRepository:
    def listar_marcados(self, id_usuario, id_trilha):
        resultado = db.session.execute(
            text("CALL sp_checklist_usuario(:id_usuario, :id_trilha)"),
            {"id_usuario": id_usuario, "id_trilha": id_trilha},
        )
        try:
            return [dict(linha) for linha in resultado.mappings().all()]
        finally:
            resultado.close()
