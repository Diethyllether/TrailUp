"""Exporta e registra os modelos ORM do pacote."""

from .avaliacao_model import Avaliacao
from .checkpoint_model import Checkpoint
from .checklist_item_model import ChecklistItem
from .denuncia_model import Denuncia
from .comentario_evento_model import ComentarioEvento
from .evento_model import Evento
from .evento_trilha_model import EventoTrilha
from .favorito_model import Favorito
from .foto_model import Foto
from .foto_registro_model import FotoRegistro
from .historico_model import HistoricoTrilha
from .notificacao_model import Notificacao
from .participante_evento_model import ParticipanteEvento
from .registro_realizado_model import RegistroRealizado
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
