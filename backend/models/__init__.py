"""Exporta e registra os modelos ORM do pacote."""

from .avaliacao_model import Avaliacao
from .checkpoint_model import Checkpoint
from .checklist_item_model import ChecklistItem
from .denuncia_model import Denuncia
from .evento_model import ComentarioEvento, Evento, EventoTrilha, ParticipanteEvento
from .favorito_model import Favorito
from .foto_model import Foto
from .historico_model import FotoRegistro, HistoricoTrilha, RegistroRealizado
from .notificacao_model import Notificacao
from .trilha_model import Trilha
from .usuario_model import Usuario

__all__ = [
    "Avaliacao",
    "Checkpoint",
    "ChecklistItem",
    "ComentarioEvento",
    "Denuncia",
    "Evento",
    "EventoTrilha",
    "Favorito",
    "Foto",
    "FotoRegistro",
    "HistoricoTrilha",
    "Notificacao",
    "ParticipanteEvento",
    "RegistroRealizado",
    "Trilha",
    "Usuario",
]
