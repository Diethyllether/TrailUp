"""Repositories especializados para consultas que envolvem múltiplas entidades."""

from .checklist_repository import ChecklistRepository
from .checkpoint_repository import CheckpointRepository
from .evento_repository import EventoRepository
from .relatorio_repository import RelatorioRepository
from .trilha_repository import TrilhaRepository

__all__ = [
    "ChecklistRepository",
    "CheckpointRepository",
    "EventoRepository",
    "RelatorioRepository",
    "TrilhaRepository",
]
