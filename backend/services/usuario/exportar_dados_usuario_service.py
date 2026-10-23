"""Caso de uso: exportar todos os dados do usuário (portabilidade, LGPD art. 18, V)."""
from datetime import datetime

from models.avaliacao_model import Avaliacao
from models.checklist_usuario_model import ChecklistUsuario
from models.comentario_evento_model import ComentarioEvento
from models.denuncia_model import Denuncia
from models.evento_model import Evento
from models.participante_evento_model import ParticipanteEvento
from models.usuario_model import Usuario
from repositories.favorito_repository import FavoritoRepository
from repositories.historico_repository import HistoricoRepository
from utils.excecoes import RecursoNaoEncontrado


class ExportarDadosUsuarioService:
    def __init__(
        self,
        modelo_usuario=None,
        modelo_avaliacao=None,
        modelo_evento=None,
        modelo_participante=None,
        modelo_comentario=None,
        modelo_denuncia=None,
        modelo_checklist=None,
        favorito_repository=None,
        historico_repository=None,
    ):
        self.modelo_usuario = modelo_usuario or Usuario
        self.modelo_avaliacao = modelo_avaliacao or Avaliacao
        self.modelo_evento = modelo_evento or Evento
        self.modelo_participante = modelo_participante or ParticipanteEvento
        self.modelo_comentario = modelo_comentario or ComentarioEvento
        self.modelo_denuncia = modelo_denuncia or Denuncia
        self.modelo_checklist = modelo_checklist or ChecklistUsuario
        self.favorito_repository = favorito_repository or FavoritoRepository()
        self.historico_repository = historico_repository or HistoricoRepository()

    def executar(self, id_usuario):
        usuario = self.modelo_usuario.buscar_por_id(id_usuario)
        if usuario is None:
            raise RecursoNaoEncontrado("usuário não encontrado")

        # A senha (hash) nunca é exportada: to_dict() já a omite por padrão.
        perfil = {
            **usuario.to_dict(),
            "termoAceitoEm": usuario.termoAceitoEm.isoformat() if usuario.termoAceitoEm else None,
            "versaoTermo": usuario.versaoTermo,
        }
        return {
            "exportadoEm": datetime.now().isoformat(timespec="seconds"),
            "perfil": perfil,
            "favoritos": self.favorito_repository.listar_por_usuario(id_usuario),
            "avaliacoes": [a.to_dict() for a in self.modelo_avaliacao.listar_por_usuario(id_usuario)],
            "historico": self.historico_repository.listar_por_usuario(id_usuario),
            "checklist": [c.to_dict() for c in self.modelo_checklist.listar_por_usuario(id_usuario)],
            "expedicoesCriadas": [e.to_dict() for e in self.modelo_evento.listar_por_criador(id_usuario)],
            "participacoes": [p.to_dict() for p in self.modelo_participante.listar_por_usuario(id_usuario)],
            "comentariosEmExpedicoes": [c.to_dict() for c in self.modelo_comentario.listar_por_usuario(id_usuario)],
            "reportesEnviados": [d.to_dict() for d in self.modelo_denuncia.listar_por_denunciante(id_usuario)],
        }
