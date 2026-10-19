from datetime import date, datetime, time

from models.evento_model import Evento
from models.evento_trilha_model import EventoTrilha
from models.participante_evento_model import ParticipanteEvento
from repositories.checkpoint_repository import CheckpointRepository
from repositories.evento_repository import EventoRepository
from services.evento.serializacao import evento_completo
from utils.excecoes import ErroDeValidacao


def _data(valor):
    if valor in (None, ""):
        return None
    return valor if isinstance(valor, date) else date.fromisoformat(str(valor))


def _horario(dia, valor):
    if valor in (None, "") or dia is None:
        return None
    if isinstance(valor, datetime):
        return valor
    hora = valor if isinstance(valor, time) else time.fromisoformat(str(valor))
    return datetime.combine(dia, hora)


class CriarEventoService:
    def __init__(self, modelo_evento=None, repository_checkpoint=None, repository_evento=None):
        self.modelo_evento = modelo_evento or Evento
        self.repository_checkpoint = repository_checkpoint or CheckpointRepository()
        self.repository_evento = repository_evento or EventoRepository()

    def executar(self, id_criador, dados):
        titulo = (dados.get("titulo") or "").strip()
        tipo = dados.get("tipo", "GRUPO")
        if not titulo or tipo not in ("INDIVIDUAL", "GRUPO"):
            raise ErroDeValidacao("título e tipo válido são obrigatórios")
        try:
            vagas = int(dados["vagas"]) if dados.get("vagas") not in (None, "") else None
            if vagas is not None and vagas < 1:
                raise ErroDeValidacao("vagas deve ser maior que zero")
            dia = _data(dados.get("data"))
            saida = _horario(dia, dados.get("horario", dados.get("horarioSaida")))
        except (TypeError, ValueError) as error:
            raise ErroDeValidacao("data, horário ou vagas inválidos") from error

        ids_trilha = dados.get("trilhas") or (
            [dados["idTrilha"]] if dados.get("idTrilha") else []
        )
        try:
            ids_trilha = [int(id_trilha) for id_trilha in ids_trilha]
        except (TypeError, ValueError) as error:
            raise ErroDeValidacao("trilha inválida") from error
        latitude, longitude = dados.get("latitude"), dados.get("longitude")
        if latitude is None or longitude is None:
            for id_trilha in ids_trilha:
                checkpoint = self.repository_checkpoint.primeiro_valido_por_trilha(id_trilha)
                if checkpoint:
                    latitude = latitude if latitude is not None else checkpoint["latitude"]
                    longitude = longitude if longitude is not None else checkpoint["longitude"]
                    break

        evento = self.modelo_evento(
            titulo=titulo, descricao=dados.get("descricao"), data=dia,
            horarioSaida=saida, imediata=bool(dados.get("imediata", False)),
            vagas=vagas, tipo=tipo, latitude=latitude, longitude=longitude,
            idCriador=id_criador,
        ).salvar()
        for id_trilha in ids_trilha:
            EventoTrilha(idEvento=evento.idEvento, idTrilha=id_trilha).salvar()
        ParticipanteEvento(idUsuario=id_criador, idEvento=evento.idEvento).salvar()
        return evento_completo(evento, self.repository_evento)
