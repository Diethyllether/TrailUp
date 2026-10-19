from datetime import date, datetime, time

from models.evento_model import Evento
from repositories.evento_repository import EventoRepository
from services.evento.serializacao import evento_completo
from utils.excecoes import ErroDeValidacao, PermissaoNegada, RecursoNaoEncontrado


class AtualizarEventoService:
    def __init__(self, modelo_evento=None, repository=None):
        self.modelo_evento = modelo_evento or Evento
        self.repository = repository or EventoRepository()

    def executar(self, id_evento, id_usuario, dados):
        evento = self.modelo_evento.buscar_por_id(id_evento)
        if evento is None:
            raise RecursoNaoEncontrado("evento não encontrado")
        if evento.idCriador != id_usuario:
            raise PermissaoNegada("apenas o criador pode editar a expedição")
        titulo = dados.get("titulo", evento.titulo)
        tipo = dados.get("tipo", evento.tipo)
        vagas = dados.get("vagas", evento.vagas)
        if not str(titulo or "").strip():
            raise ErroDeValidacao("título é obrigatório")
        if tipo not in ("INDIVIDUAL", "GRUPO"):
            raise ErroDeValidacao("tipo deve ser INDIVIDUAL ou GRUPO")
        try:
            if vagas not in (None, ""):
                vagas = int(vagas)
                if vagas < 1:
                    raise ErroDeValidacao("vagas deve ser maior que zero")
            elif "vagas" in dados:
                vagas = None
            if "data" in dados:
                dia = date.fromisoformat(dados["data"]) if dados["data"] else None
                evento.data = dia
            else:
                dia = evento.data
            if "horario" in dados or "horarioSaida" in dados:
                valor_horario = dados.get("horario", dados.get("horarioSaida"))
                if valor_horario in (None, ""):
                    evento.horarioSaida = None
                elif isinstance(valor_horario, datetime):
                    evento.horarioSaida = valor_horario
                else:
                    hora = time.fromisoformat(str(valor_horario))
                    evento.horarioSaida = datetime.combine(dia, hora) if dia else None
        except (TypeError, ValueError) as error:
            raise ErroDeValidacao("data, horário ou vagas inválidos") from error
        for campo in ("titulo", "descricao", "imediata", "latitude", "longitude"):
            if campo in dados:
                setattr(evento, campo, dados[campo])
        evento.tipo = tipo
        evento.vagas = vagas
        return evento_completo(evento.atualizar(), self.repository)
