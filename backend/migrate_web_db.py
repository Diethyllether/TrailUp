"""Atualiza bancos TrailUp antigos para o schema esperado pela versão web.

Uso:
    cd backend
    python migrate_web_db.py

O script preserva os dados existentes. Ele cria tabelas ausentes com
SQLAlchemy e adiciona apenas as colunas conhecidas que faltam em bancos
criados por versões anteriores do projeto.
"""
from sqlalchemy import inspect, text

from app import create_app
from extensions import db


app = create_app()


def _column_names(inspector, table_name):
    return {column["name"] for column in inspector.get_columns(table_name)}


def _add_column_if_missing(connection, inspector, table_name, column_name, ddl):
    if table_name not in inspector.get_table_names():
        return False
    if column_name in _column_names(inspector, table_name):
        return False
    connection.execute(text(f"ALTER TABLE `{table_name}` ADD COLUMN {ddl}"))
    print(f"+ {table_name}.{column_name}")
    return True


with app.app_context():
    # Cria tabelas completamente ausentes, como favorito em bancos bem antigos.
    db.create_all()

    engine = db.engine
    inspector = inspect(engine)

    # Colunas necessárias para a versão atual da entidade Trilha.
    alterations = [
        ("trilha", "imagemUrl", "`imagemUrl` VARCHAR(255) NULL"),
        ("trilha", "tempoEstimadoMin", "`tempoEstimadoMin` FLOAT NULL"),

        # Campos usados na criação/listagem de expedições e no Google Maps.
        ("evento", "horarioSaida", "`horarioSaida` DATETIME NULL"),
        ("evento", "imediata", "`imediata` BOOLEAN NOT NULL DEFAULT 0"),
        ("evento", "latitude", "`latitude` FLOAT NULL"),
        ("evento", "longitude", "`longitude` FLOAT NULL"),

        # Compatibilidade com recursos auxiliares atuais da API.
        ("notificacao", "idUsuario", "`idUsuario` INT NULL"),
        ("denuncia", "idUsuarioDenunciante", "`idUsuarioDenunciante` INT NULL"),
        ("denuncia", "idUsuarioDenunciado", "`idUsuarioDenunciado` INT NULL"),
        ("historicoTrilha", "idUsuario", "`idUsuario` INT NULL"),
    ]

    changed = False
    with engine.begin() as connection:
        for table_name, column_name, ddl in alterations:
            # Atualiza o inspector depois de cada alteração para refletir o schema novo.
            inspector = inspect(connection)
            changed |= _add_column_if_missing(
                connection,
                inspector,
                table_name,
                column_name,
                ddl,
            )

    print("Schema atualizado com sucesso." if changed else "Schema já estava atualizado.")
