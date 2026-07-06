"""
Importa todos os models para que o SQLAlchemy os registre em db.metadata
(necessário para db.create_all() e para a resolução das ForeignKeys).
"""
from models.usuario_model import Usuario
from models.trilha_model import Trilha
from models.avaliacao_model import Avaliacao
from models.favorito_model import Favorito
from models.checkpoint_model import Checkpoint
from models.foto_model import Foto
from models.mapa_offline_model import MapaOffline
from models.evento_model import Evento, EventoTrilha, ParticipanteEvento
from models.notificacao_model import Notificacao
from models.denuncia_model import Denuncia
from models.historico_model import HistoricoTrilha, RegistroRealizado, FotoRegistro

__all__ = [
    "Usuario",
    "Trilha",
    "Avaliacao",
    "Favorito",
    "Checkpoint",
    "Foto",
    "MapaOffline",
    "Evento",
    "EventoTrilha",
    "ParticipanteEvento",
    "Notificacao",
    "Denuncia",
    "HistoricoTrilha",
    "RegistroRealizado",
    "FotoRegistro",
]
