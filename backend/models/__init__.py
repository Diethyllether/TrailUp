"""Exporta e registra os modelos ORM do pacote."""

from .avaliacao_model import Avaliacao
from .checkpoint_model import Checkpoint
from .checklist_item_model import ChecklistItem
from .checklist_usuario_model import ChecklistUsuario
from .denuncia_model import Denuncia
from .comentario_evento_model import ComentarioEvento
from .evento_model import Evento
from .evento_trilha_model import EventoTrilha
from .favorito_model import Favorito
from .historico_model import HistoricoTrilha
from .participante_evento_model import ParticipanteEvento
from .trilha_model import Trilha
from .token_recuperacao_model import TokenRecuperacao
from .usuario_model import Usuario

__all__ = [
    "Avaliacao",
    "Checkpoint",
    "ChecklistItem",
    "ChecklistUsuario",
    "ComentarioEvento",
    "Denuncia",
    "Evento",
    "EventoTrilha",
    "Favorito",
    "HistoricoTrilha",
    "ParticipanteEvento",
    "Trilha",
    "TokenRecuperacao",
    "Usuario",
]
