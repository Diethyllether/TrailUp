# Fluxograma — criar expedição

```mermaid
flowchart TD
  A[Tela Expedições: formulário] -->|fetch POST /api/events| B[evento_bp]
  B --> C[EventoController.criar]
  C --> D[CriarEventoService.executar]
  D --> E{Coordenadas recebidas?}
  E -- Não --> F[CheckpointRepository.primeiro_valido_por_trilha]
  F -->|CALL sp_primeiro_checkpoint_valido| G[(MySQL)]
  G --> H[Usar coordenadas do primeiro checkpoint válido]
  E -- Sim --> I[Usar coordenadas informadas]
  H --> J[Evento.salvar e vínculos pelas Models]
  I --> J
  J --> K[EventoRepository.detalhes_em_lote]
  K -->|CALL sp_detalhes_eventos| G
  G --> L[EventoController devolve JSON]
  L --> A
```

Se a trilha não tiver checkpoint válido, a expedição ainda pode ser criada sem coordenadas herdadas. A resposta é montada com os detalhes do evento consultados pelo Repository.
