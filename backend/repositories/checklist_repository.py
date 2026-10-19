from sqlalchemy import text

from extensions import db
from models.checklist_item_model import ChecklistItem
from models.checklist_usuario_model import ChecklistUsuario


class ChecklistRepository:
    def listar_marcados(self, id_usuario, id_trilha):
        if db.session.get_bind().dialect.name != "mysql":
            return [
                {"idChecklistItem": row.idChecklistItem, "marcado": row.marcado}
                for row in ChecklistUsuario.query.join(
                    ChecklistItem,
                    ChecklistItem.idChecklistItem == ChecklistUsuario.idChecklistItem,
                ).filter(
                    ChecklistUsuario.idUsuario == id_usuario,
                    ChecklistItem.idTrilha == id_trilha,
                ).all()
            ]

        resultado = db.session.execute(
            text("CALL sp_checklist_usuario(:id_usuario, :id_trilha)"),
            {"id_usuario": id_usuario, "id_trilha": id_trilha},
        )
        try:
            return [dict(linha) for linha in resultado.mappings().all()]
        finally:
            resultado.close()
