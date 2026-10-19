# Fluxograma — participar de expedição

```mermaid
flowchart TD
  A[Tela de expedições] --> B[fetch POST /api/events/id/participation]
  B --> C[Rota em api_controller.py]
  C --> D[EventoService.participar]
  D --> E[EventoRepository consulta evento e participantes]
  E --> F{Evento existe e há vaga?}
  F -- Não --> G[Erro de domínio / resposta HTTP]
  F -- Sim --> H[ParticipanteEvento.salvar]
  H --> I[(MySQL)]
  I --> J[JSON de sucesso]
  J --> A
```

O caminho atual utiliza ORM no repository; `sp_contar_participantes_evento` ainda não existe em `procedures.sql`. A validação de vagas é implementada no Service e não deve ser confundida com uma procedure já implantada.
