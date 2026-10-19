from models.avaliacao_model import Avaliacao
from models.checklist_item_model import ChecklistItem
from models.checkpoint_model import Checkpoint
from models.favorito_model import Favorito
from models.trilha_model import Trilha
from repositories.evento_repository import EventoRepository
from repositories.trilha_repository import TrilhaRepository
from utils.excecoes import RecursoNaoEncontrado


class DetalharTrilhaService:
    def __init__(self, repository=None, evento_repository=None):
        self.repository = repository or TrilhaRepository()
        self.evento_repository = evento_repository or EventoRepository()

    def executar(self, id_trilha, id_usuario=None):
        trilha = Trilha.buscar_por_id(id_trilha)
        if not trilha:
            raise RecursoNaoEncontrado("trilha não encontrada")
        avaliacoes = self.repository.avaliacoes_com_autores(id_trilha)
        registros = [
            {**avaliacao.to_dict(), "nomeUsuario": nome}
            for avaliacao, nome in avaliacoes
        ]
        favoritos = Favorito.listar_por_usuario(id_usuario) if id_usuario else []
        media, _quantidade = self.repository.medias_avaliacao().get(id_trilha, (None, 0))
        eventos = self.evento_repository.listar_por_trilha(id_trilha)
        detalhes_eventos = self.evento_repository.detalhes_em_lote(
            [evento.idEvento for evento in eventos]
        )
        return {
            "trail": trilha.to_dict(),
            "checkpoints": [item.to_dict() for item in Checkpoint.listar_por_trilha(id_trilha)],
            "events": [
                {**evento.to_dict(), **detalhes_eventos.get(evento.idEvento, {})}
                for evento in eventos
            ],
            "reviews": registros,
            "checklist": [item.to_dict() for item in ChecklistItem.listar_por_trilha(id_trilha)],
            "favorite": any(item.idTrilha == id_trilha for item in favoritos),
            "average": float(media) if media is not None else None,
        }
