# Fluxograma — ranking de trilheiros

```mermaid
flowchart LR
  A[Tela Ranking] --> B[fetch GET /api/reports/ranking]
  B --> C[Rota ranking_usuarios em api_controller.py]
  C --> D[RelatorioService.ranking_usuarios]
  D --> E[RelatorioRepository.ranking_usuarios]
  E --> F[CALL sp_ranking_usuarios]
  F --> G[(MySQL)]
  G --> H[list de dict]
  H --> I[JSON]
  I --> A
```

A rota e tela existem. A execução da procedure precisa ser validada com um servidor MySQL; a verificação disponível neste ambiente foi por chamadas simuladas ao controller.
