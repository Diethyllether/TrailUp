from models.checklist_item_model import ChecklistItem
from models.checklist_usuario_model import ChecklistUsuario
from utils.excecoes import ErroDeValidacao, RecursoNaoEncontrado


class MarcarItemChecklistService:
    def __init__(self, modelo_item=None, modelo_usuario=None):
        self.modelo_item = modelo_item or ChecklistItem
        self.modelo_usuario = modelo_usuario or ChecklistUsuario

    def executar(self, id_usuario, id_item, marcado):
        if not isinstance(marcado, bool):
            raise ErroDeValidacao("marcado deve ser verdadeiro ou falso")
        if self.modelo_item.buscar_por_id(id_item) is None:
            raise RecursoNaoEncontrado("item do checklist não encontrado")
        registro = self.modelo_usuario.buscar(id_usuario, id_item)
        if registro is None:
            registro = self.modelo_usuario(
                idUsuario=id_usuario, idChecklistItem=id_item, marcado=marcado
            ).salvar()
        else:
            registro.marcado = marcado
            registro.atualizar()
        return registro.to_dict()
