"""Teste unitário do caso de uso de exportação de dados (sem banco)."""
import datetime
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.usuario.exportar_dados_usuario_service import ExportarDadosUsuarioService
from utils.excecoes import RecursoNaoEncontrado


class Item:
    def __init__(self, **dados):
        self.dados = dados

    def to_dict(self):
        return self.dados


class FakeUsuario:
    usuario = SimpleNamespace(
        termoAceitoEm=datetime.datetime(2026, 10, 1, 12, 0),
        versaoTermo="2.0",
        to_dict=lambda: {"idUsuario": 1, "nome": "Ana", "email": "ana@x.com"},
    )

    @classmethod
    def buscar_por_id(cls, id_usuario):
        return cls.usuario if id_usuario == 1 else None


def fake_modelo(chave):
    class Fake:
        pass

    for nome in ("listar_por_usuario", "listar_por_criador", "listar_por_denunciante"):
        setattr(Fake, nome, classmethod(lambda cls, _id: [Item(tipo=chave)]))
    return Fake


class FakeRepo:
    def listar_por_usuario(self, _id):
        return [{"item": "repo"}]


def criar_servico():
    return ExportarDadosUsuarioService(
        modelo_usuario=FakeUsuario,
        modelo_avaliacao=fake_modelo("avaliacao"),
        modelo_evento=fake_modelo("evento"),
        modelo_participante=fake_modelo("participante"),
        modelo_comentario=fake_modelo("comentario"),
        modelo_denuncia=fake_modelo("denuncia"),
        modelo_checklist=fake_modelo("checklist"),
        favorito_repository=FakeRepo(),
        historico_repository=FakeRepo(),
    )


def test_exporta_todas_as_secoes_sem_senha():
    dados = criar_servico().executar(1)
    assert dados["perfil"]["versaoTermo"] == "2.0"
    assert "senha" not in dados["perfil"]
    for secao in (
        "favoritos", "avaliacoes", "historico", "checklist",
        "expedicoesCriadas", "participacoes", "comentariosEmExpedicoes", "reportesEnviados",
    ):
        assert dados[secao], secao


def test_usuario_inexistente():
    with pytest.raises(RecursoNaoEncontrado):
        criar_servico().executar(99)
