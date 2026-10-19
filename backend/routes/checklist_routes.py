from flask import Blueprint

from controllers.checklist_controller import ChecklistController
from utils.decorators import login_obrigatorio

checklist_bp = Blueprint("checklist", __name__)


@checklist_bp.get("/trails/<int:id_trilha>/checklist-state")
@login_obrigatorio
def consultar_checklist(id_trilha):
    return ChecklistController.consultar(id_trilha)


@checklist_bp.patch("/checklist/<int:id_item>")
@login_obrigatorio
def marcar_item(id_item):
    return ChecklistController.marcar(id_item)
