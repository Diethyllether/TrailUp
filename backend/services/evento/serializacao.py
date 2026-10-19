def evento_completo(evento, repository):
    detalhes = repository.detalhes_em_lote([evento.idEvento]).get(evento.idEvento, {})
    return {**evento.to_dict(), **detalhes}
