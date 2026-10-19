"""Repositories especializados para consultas que envolvem múltiplas entidades."""

from .checklist_repository import ChecklistRepository
from .checkpoint_repository import CheckpointRepository
from .evento_repository import EventoRepository
from .favorito_repository import FavoritoRepository
from .historico_repository import HistoricoRepository
from .relatorio_repository import RelatorioRepository
from .trilha_repository import TrilhaRepository

__all__ = [
    "ChecklistRepository",
    "CheckpointRepository",
    "EventoRepository",
    "FavoritoRepository",
    "HistoricoRepository",
    "RelatorioRepository",
    "TrilhaRepository",
]
