"""Integração das stored procedures com MySQL 8 e o seed do TrailUp."""

import os
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text


@pytest.fixture(scope="module")
def conexao_mysql():
    url = os.environ.get("DATABASE_URL")
    if not url:
        pytest.fail("Defina DATABASE_URL para um banco MySQL 8 com schema, procedures e seed.")

    engine = create_engine(url)
    if engine.dialect.name != "mysql":
        engine.dispose()
        pytest.fail("test_procedures.py exige MySQL; SQLite não executa stored procedures.")

    with engine.connect() as conexao:
        yield conexao
    engine.dispose()


def chamar(conexao, sql, parametros=None):
    resultado = conexao.execute(text(sql), parametros or {})
    try:
        return [dict(linha) for linha in resultado.mappings().all()]
    finally:
        resultado.close()


def test_procedures_do_seed(conexao_mysql):
    trilhas = chamar(
        conexao_mysql,
        "CALL sp_buscar_trilhas(:termo, :dificuldade)",
        {"termo": "Pedra Bonita", "dificuldade": None},
    )
    assert trilhas
    id_trilha = trilhas[0]["idTrilha"]

    filtradas = chamar(
        conexao_mysql,
        "CALL sp_filtrar_trilhas(:distancia, :duracao, :nota, :ordem)",
        {"distancia": None, "duracao": None, "nota": None, "ordem": "nome"},
    )
    assert any(item["idTrilha"] == id_trilha for item in filtradas)

    medias = chamar(conexao_mysql, "CALL sp_medias_trilhas()")
    assert any(item["idTrilha"] == id_trilha for item in medias)
    assert chamar(conexao_mysql, "CALL sp_avaliacoes_trilha(:id)", {"id": id_trilha}) == []
    assert chamar(conexao_mysql, "CALL sp_historico_usuario(:id)", {"id": 0}) == []

    pontos = chamar(conexao_mysql, "CALL sp_checkpoints_validos()")
    assert any(item["idTrilha"] == id_trilha for item in pontos)
    pontos_trilha = chamar(
        conexao_mysql, "CALL sp_checkpoints_trilha(:id)", {"id": id_trilha}
    )
    assert pontos_trilha
    assert chamar(
        conexao_mysql, "CALL sp_primeiro_checkpoint_valido(:id)", {"id": id_trilha}
    )

    assert chamar(conexao_mysql, "CALL sp_trilhas_evento(:id)", {"id": 0}) == []
    assert chamar(conexao_mysql, "CALL sp_eventos_por_trilha(:id)", {"id": id_trilha}) == []
    assert chamar(conexao_mysql, "CALL sp_eventos_por_usuario(:id)", {"id": 0}) == []
    assert chamar(conexao_mysql, "CALL sp_participantes_evento(:id)", {"id": 0}) == []
    assert chamar(conexao_mysql, "CALL sp_comentarios_evento(:id)", {"id": 0}) == []
    assert chamar(
        conexao_mysql, "CALL sp_contar_participantes_evento(:id)", {"id": 0}
    )[0]["quantidade"] == 0
    assert chamar(
        conexao_mysql,
        "CALL sp_detalhes_eventos(:ids)",
        {"ids": "[]"},
    ) == []

    assert chamar(conexao_mysql, "CALL sp_resumo_usuario(:id)", {"id": 0}) == []
    assert chamar(conexao_mysql, "CALL sp_ranking_usuarios(:limite)", {"limite": 10}) == []
    assert chamar(conexao_mysql, "CALL sp_favoritos_usuario(:id)", {"id": 0}) == []
    assert chamar(conexao_mysql, "CALL sp_eventos_ativos()") == []
    assert chamar(
        conexao_mysql,
        "CALL sp_checklist_usuario(:usuario, :trilha)",
        {"usuario": 0, "trilha": id_trilha},
    ) == []
    proximas = chamar(
        conexao_mysql,
        "CALL sp_trilhas_proximas(:latitude, :longitude, :limite)",
        {"latitude": -22.985748, "longitude": -43.279124, "limite": 10},
    )
    assert any(item["idTrilha"] == id_trilha for item in proximas)

    sql = Path(__file__).parents[1].joinpath("database", "procedures.sql").read_text(
        encoding="utf-8"
    )
    assert "CREATE PROCEDURE sp_trilhas_por_dificuldade" not in sql
