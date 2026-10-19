# Fluxograma — cadastrar usuário com aceite

```mermaid
flowchart TD
  A[Tela de cadastro e checkbox] --> B[fetch POST /api/auth/register com aceitouTermo]
  B --> C[Rota register em api_controller.py]
  C --> D[UsuarioService.criar]
  D --> E{aceitouTermo é true?}
  E -- Não --> F[Erro HTTP 400]
  E -- Sim --> G[Usuario.salvar com termoAceitoEm e versaoTermo]
  G --> H[(MySQL)]
  H --> I[JSON e sessão]
  I --> A
```

A aplicação registra a decisão e a versão do termo. O arquivo PDF correto ainda não foi fornecido, portanto a rota do documento não pode ser considerada validada.
