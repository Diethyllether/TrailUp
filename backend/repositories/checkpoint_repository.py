"""Consultas de geolocalização que dependem de validação ou agregação."""

from sqlalchemy import text

from extensions import db


class CheckpointRepository:
    def listar_por_trilha(self, id_trilha):
        resultado = db.session.execute(
            text("CALL sp_checkpoints_trilha(:id_trilha)"), {"id_trilha": id_trilha}
        )
        try:
            return [dict(linha) for linha in resultado.mappings().all()]
        finally:
            resultado.close()

    def primeiro_valido_por_trilha(self, id_trilha):
        resultado = db.session.execute(
            text("CALL sp_primeiro_checkpoint_valido(:id_trilha)"),
            {"id_trilha": id_trilha},
        )
        try:
            linhas = [dict(linha) for linha in resultado.mappings().all()]
            return linhas[0] if linhas else None
        finally:
            resultado.close()
