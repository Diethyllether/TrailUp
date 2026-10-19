"""Repositories especializados para consultas que envolvem múltiplas entidades."""

from .checkpoint_repository import CheckpointRepository
from .evento_repository import EventoRepository
from .relatorio_repository import RelatorioRepository
from .trilha_repository import TrilhaRepository

__all__ = [
    "CheckpointRepository",
    "EventoRepository",
    "RelatorioRepository",
    "TrilhaRepository",
]
