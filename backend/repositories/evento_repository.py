"""Consultas de eventos, vínculos e participantes por procedures MySQL."""

import json

from sqlalchemy import text

from extensions import db
from models.evento_model import Evento


def _executar(call_sql, parametros):
    resultado = db.session.execute(text(call_sql), parametros)
    try:
        return [dict(linha) for linha in resultado.mappings().all()]
    finally:
        resultado.close()


def _evento_da_linha(linha):
    campos = {
        "idEvento", "titulo", "descricao", "data", "horarioSaida", "imediata",
        "vagas", "tipo", "latitude", "longitude", "idCriador",
    }
    evento = Evento(**{chave: valor for chave, valor in linha.items() if chave in campos})
    for campo in ("nomeCriador", "participantesAtuais", "trilhas"):
        if campo in linha:
            setattr(evento, campo, linha[campo])
    return evento


def _json_da_linha(valor):
    if isinstance(valor, str):
        return json.loads(valor)
    return valor


class EventoRepository:
    """Acesso especializado a eventos, participantes e comentários."""

    model = Evento

    def listar_ativos(self):
        return [_evento_da_linha(linha) for linha in _executar("CALL sp_eventos_ativos()", {})]

    def listar_por_trilha(self, id_trilha):
        linhas = _executar(
            "CALL sp_eventos_por_trilha(:id_trilha)", {"id_trilha": id_trilha}
        )
        return [_evento_da_linha(linha) for linha in linhas]

    def contar_participantes(self, id_evento):
        linhas = _executar(
            "CALL sp_contar_participantes_evento(:id_evento)", {"id_evento": id_evento}
        )
        return int(linhas[0]["quantidade"]) if linhas else 0

    def detalhes_em_lote(self, ids_evento):
        if not ids_evento:
            return {}
        linhas = _executar(
            "CALL sp_detalhes_eventos(:ids_evento)",
            {"ids_evento": json.dumps(ids_evento)},
        )
        return {
            linha["idEvento"]: {
                "trilhasIds": _json_da_linha(linha["trilhasIds"]) or [],
                "participantes": _json_da_linha(linha["participantes"]) or [],
                "participantesAtuais": linha["participantesAtuais"] or 0,
                "comentarios": _json_da_linha(linha["comentarios"]) or [],
                "nomeCriador": linha["nomeCriador"],
            }
            for linha in linhas
        }
