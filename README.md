# TrailUp

Aplicação web para descobrir trilhas, consultar percursos e checkpoints, avaliar trilhas, salvar favoritos e organizar eventos em grupo.

O projeto tem frontend estático em HTML, CSS e JavaScript e uma API REST em Flask. Os dados são armazenados em MySQL; os mapas das trilhas são renderizados com MapLibre GL e tiles do OpenStreetMap.

```text
Navegador (frontend) ⇄ API Flask (/api) → Services → Repositories/SQLAlchemy → MySQL
```

## Funcionalidades Implementadas

| Caso de uso | Tipo | Rota | Tela |
|---|---|---|---|
| Consultar sessão atual | [Consulta/Repository] | `GET /session` | Inicialização da aplicação |
| Cadastrar usuário com aceite do termo | [CRUD] | `POST /auth/register` | Cadastro |
| Autenticar usuário | [Consulta/Repository] | `POST /auth/login` | Login |
| Encerrar sessão | [CRUD] | `POST /auth/logout` | Navegação |
| Buscar trilhas por texto e dificuldade | [Consulta/Repository] | `GET /trails` | Home |
| Filtrar e ordenar trilhas | [Consulta/Repository] | `GET /trails` | Filtros da home |
| Buscar trilhas próximas | [Consulta/Repository] | `GET /trails?lat=…&lon=…` | Botão “Trilhas próximas” |
| Consultar detalhes, checkpoints e avaliações | [Consulta/Repository] | `GET /trails/<trail_id>` | Detalhe da trilha |
| Adicionar trilha aos favoritos | [CRUD] | `POST /trails/<trail_id>/favorite` | Cards e detalhe |
| Remover trilha dos favoritos | [CRUD] | `DELETE /trails/<trail_id>/favorite` | Cards e detalhe |
| Consultar favoritos | [Consulta/Repository] | `GET /favorites` | Favoritos |
| Consultar expedições e participantes | [Consulta/Repository] | `GET /events` | Expedições |
| Criar expedição | [CRUD] | `POST /events` | Formulário de expedição |
| Participar de expedição com validação de vagas | [Consulta/Repository] | `POST /events/<event_id>/participation` | Expedições |
| Sair de expedição | [CRUD] | `DELETE /events/<event_id>/participation` | Expedições |
| Editar expedição própria | [CRUD] | `PUT /events/<event_id>` | Expedições |
| Cancelar expedição própria | [CRUD] | `DELETE /events/<event_id>` | Expedições |
| Comentar como participante confirmado | [CRUD] | `POST /events/<event_id>/comments` | Expedições |
| Publicar avaliação | [CRUD] | `POST /trails/<trail_id>/reviews` | Detalhe da trilha |
| Editar avaliação própria | [CRUD] | `PUT /reviews/<review_id>` | Detalhe da trilha |
| Excluir avaliação própria | [CRUD] | `DELETE /reviews/<review_id>` | Detalhe da trilha |
| Consultar histórico de trilhas | [Consulta/Repository] | `GET /history` | Perfil |
| Registrar trilha concluída | [CRUD] | `POST /history` | Detalhe da trilha |
| Atualizar perfil | [CRUD] | `PATCH /profile` | Perfil |
| Reportar problema | [CRUD] | `POST /reports` | Home, trilha e expedição |
| Solicitar recuperação de senha | [Consulta/Repository] | `POST /auth/password-reset` | Recuperar senha |
| Redefinir senha com token de uso único | [CRUD] | `POST /auth/password-reset/confirm` | Redefinir senha |
| Consultar ranking de trilheiros | [Consulta/Repository] | `GET /reports/ranking` | Ranking |
| Consultar resumo pessoal | [Consulta/Repository] | `GET /reports/summary` | Resumo |
| Consultar estado do checklist da trilha | [Consulta/Repository] | `GET /trails/<trail_id>/checklist-state` | Detalhe da trilha |
| Salvar marcação de equipamento | [CRUD] | `PATCH /checklist/<item_id>` | Detalhe da trilha |

O checklist de equipamentos é salvo por usuário no banco de dados. O PDF correto do termo de consentimento ainda depende de ser fornecido para disponibilizar o documento e concluir a validação do cadastro.

## Tecnologias

- Python, Flask e Flask-SQLAlchemy
- MySQL com PyMySQL
- HTML, CSS e JavaScript
- MapLibre GL e OpenStreetMap (necessários para exibir mapas; carregados pela internet)

## Requisitos para executar

- Python 3.10 ou superior
- MySQL 8 ou superior
- Navegador moderno

## Instalação e execução

Abra dois terminais na raiz do projeto. Os exemplos abaixo usam PowerShell.

### 1. Criar o banco

Inicie o MySQL e execute o esquema:

```powershell
mysql -u root -p < backend/database/create_database.sql
```

Opcionalmente, carregue dados de demonstração:

```powershell
mysql -u root -p trilhas_db < backend/database/seed_dados_exemplo.sql
```

O seed SQL inclui uma trilha real, Pedra Bonita (RJ), e um registro fictício identificado como demonstração. Cadastre uma conta pela interface para usar recursos que exigem autenticação.

### 2. Iniciar a API Flask

No primeiro terminal:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edite .env com a URL do banco e uma SECRET_KEY aleatória.
# Configure SMTP para enviar links de recuperação de senha
$env:SMTP_HOST = "smtp.exemplo.com"
$env:SMTP_PORT = "587"
$env:SMTP_USER = "seu-usuario"
$env:SMTP_PASSWORD = "sua-senha-de-aplicativo"
$env:SMTP_FROM = "nao-responda@exemplo.com"
$env:FRONTEND_URL = "http://localhost:8000"
python app.py
```

Sem SMTP configurado, a recuperação de senha não envia o link. A API mantém a mesma resposta genérica, e nunca inclui o token na resposta. Configure SMTP para habilitar o envio; os tokens são armazenados como hash, expiram em uma hora e só podem ser usados uma vez.

Crie um usuário MySQL próprio para a aplicação e configure sua URL em `backend/.env`. A API ficará disponível em `http://localhost:5000`.

### 3. Iniciar o frontend estático

No segundo terminal, a partir da raiz do projeto:

```powershell
cd frontend
python -m http.server 8000
```

Abra `http://localhost:8000`. O endereço da API é definido em `frontend/config.js` (por padrão, `http://localhost:5000/api`). Se mudar a porta ou o endereço do frontend, ajuste `FRONTEND_ORIGIN` no terminal da API para a origem exata.

## API REST

Base local: `http://localhost:5000/api`. As rotas recebem e retornam JSON, salvo respostas sem conteúdo. Sessões usam cookie; nas chamadas do navegador, envie credenciais. O frontend já faz isso.

| Método | Rota | Autenticação | Descrição |
|---|---|---|---|
| `GET` | `/session` | Não | Retorna o usuário da sessão atual ou `null`. |
| `POST` | `/auth/register` | Não | Cria conta e inicia sessão. JSON: `nome`, `email`, `senha` e `aceitouTermo: true`. |
| `POST` | `/auth/login` | Não | Inicia sessão. JSON: `email`, `senha`. |
| `POST` | `/auth/logout` | Não | Encerra a sessão. |
| `GET` | `/trails` | Não | Lista trilhas. Filtros: `q`, `difficulty`, `sort`, `maxDistance`, `maxDuration`, `minRating`; `lat` e `lon` limitam às próximas. |
| `GET` | `/trails/<trail_id>` | Não | Detalhes, checkpoints, eventos, avaliações, checklist e média. |
| `POST` | `/trails/<trail_id>/favorite` | Sim | Adiciona a trilha aos favoritos. |
| `DELETE` | `/trails/<trail_id>/favorite` | Sim | Remove a trilha dos favoritos. |
| `GET` | `/favorites` | Sim | Lista as trilhas favoritas do usuário. |
| `GET` | `/events` | Não | Lista eventos, estado de participação e trilhas disponíveis. |
| `POST` | `/events` | Sim | Cria evento. JSON aceita `titulo`, `descricao`, `data` (`AAAA-MM-DD`), `horario` (`HH:MM`), `imediata`, `vagas`, `tipo` e `idTrilha`. |
| `POST` | `/events/<event_id>/participation` | Sim | Participa do evento. |
| `DELETE` | `/events/<event_id>/participation` | Sim | Sai do evento. |
| `POST` | `/trails/<trail_id>/reviews` | Sim | Publica avaliação. JSON: `nota` (1 a 5) e `comentario`. |
| `PUT`, `DELETE` | `/reviews/<review_id>` | Sim | Edita ou remove avaliação própria. |
| `GET`, `POST` | `/history` | Sim | Lista o histórico e registra uma trilha concluída. |
| `PATCH` | `/profile` | Sim | Atualiza nome, e-mail e URL da foto do usuário. |
| `PUT`, `DELETE` | `/events/<event_id>` | Sim | Edita ou cancela evento próprio. |
| `POST` | `/events/<event_id>/comments` | Sim | Publica comentário como participante confirmado. |
| `POST` | `/reports` | Sim | Registra denúncia de bug, trilha, evento ou outro problema. |
| `GET` | `/reports/ranking` | Não | Ranking agregado da comunidade. |
| `GET` | `/reports/summary` | Sim | Resumo agregado do usuário autenticado. |
| `POST` | `/auth/password-reset` | Não | Solicita link de recuperação por e-mail. |
| `POST` | `/auth/password-reset/confirm` | Não | Redefine senha com token válido. |

Exemplo de busca:

```text
GET http://localhost:5000/api/trails?q=pedra&difficulty=FACIL
```

Falhas são retornadas em JSON no formato `{"error":"mensagem"}`. Rotas que exigem autenticação retornam HTTP `401` sem sessão válida. A API permite CORS somente para a origem definida em `FRONTEND_ORIGIN`.

## Mapas

O frontend usa MapLibre GL para renderizar os mapas das trilhas com tiles do OpenStreetMap. Não é necessária uma chave Google Maps. Os mapas dependem de conexão com a internet e da disponibilidade do serviço de tiles.

## Estrutura do projeto

```text
backend/
  api_controller.py       # Rotas da API JSON
  app.py                  # Configuração e inicialização Flask
  database/               # Esquema, migrações, relatórios e seed SQL
  models/                 # Modelos SQLAlchemy
  repositories/           # Acesso a dados
  services/               # Regras de negócio
  requirements.txt
frontend/
  index.html
  config.js               # Endereço da API
  static/css/
  static/js/
```

## Requisitos do projeto

1. O sistema deve permitir buscar trilhas pelo nome ou localização.
2. O sistema deve mostrar a distância, a duração e o nível de dificuldade de cada trilha.
3. O sistema deve exibir um mapa específico para cada trilha.
4. O sistema deve permitir publicar avaliações e comentários sobre trilhas.
5. O sistema deve permitir salvar trilhas como favoritas.
6. O sistema deve fornecer um checklist de equipamentos para as trilhas.
7. O sistema deve permitir criar eventos para trilhas.
8. O sistema deve registrar o histórico de trilhas realizadas.
9. O sistema deve permitir editar ou excluir a própria avaliação.
10. O sistema deve exibir a nota média da trilha, calculada a partir das avaliações.
11. O sistema deve permitir editar o perfil do usuário (nome, e-mail e foto).
12. O sistema deve listar os participantes confirmados de um evento, exibindo apenas seus nomes.
13. O sistema deve permitir ordenar ou filtrar trilhas por distância, duração ou nota.
14. O sistema deve permitir comentários em eventos para que participantes combinem detalhes.
15. O sistema deve exibir trilhas próximas ao usuário.
16. O sistema deve oferecer um botão para reportar problemas, como bugs ou informações sobre trilhas.
17. O sistema deve permitir concluir uma trilha, registrando a data, o tempo e uma avaliação pessoal.
18. O sistema deve permitir recuperar a senha por meio de telas e do envio de um link.
19. O sistema deve permitir que o organizador edite ou cancele seus eventos.
20. O sistema salva as marcações do checklist por usuário no banco de dados.
## Arquitetura e evidências

O frontend estático pode ser executado separadamente na porta 8000 e consome a API Flask na porta 5000 por `fetch`. O backend usa Services, Models SQLAlchemy com CRUD Active Record e repositories para consultas especializadas. A migração para a rubrica segue parcial: a maioria das rotas permanece em `backend/api_controller.py` e ainda há Services Facade. Ranking e resumo já usam `RelatorioController`, Blueprint próprio e Services por caso de uso.

- [Diagrama das Models existentes](docs/diagrama_de_classes.md)
- [Fluxogramas](docs/fluxogramas/)
- [Roteiro dos slides](docs/apresentacao.md)
- [Roteiro de vídeo de até 2 minutos](docs/roteiro_video.md)
- Verificador: `python scripts/verificar_arquitetura.py` (atualmente reporta violações; consultar as pendências finais).

### Procedures do banco

| Procedure | Parâmetros | Repository |
|---|---|---|
| `sp_trilhas_por_dificuldade` | dificuldade, localização, ordem | `RelatorioRepository.trilhas_ordenadas` |
| `sp_favoritos_usuario` | id do usuário | `RelatorioRepository.favoritos_usuario` |
| `sp_resumo_usuario` | id do usuário | `RelatorioRepository.resumo_usuario` |
| `sp_ranking_usuarios` | limite | `RelatorioRepository.ranking_usuarios` |
| `sp_eventos_ativos` | nenhum | `RelatorioRepository.eventos_ativos` |
| `sp_checklist_usuario` | id do usuário, id da trilha | `ChecklistRepository.listar_marcados` |
| `sp_trilhas_proximas` | latitude, longitude, limite | `TrilhaRepository.trilhas_proximas` |

A execução real dessas procedures requer MySQL. `sp_eventos_ativos` e `sp_favoritos_usuario` estão implementadas no Repository, mas ainda não foram confirmadas ligadas a uma tela específica. Trilhas próximas agora chamam `sp_trilhas_proximas` pelo Repository; o SQLite usa um fallback local para desenvolvimento.

### Models e repositories

As entidades registradas estão em `backend/models/`, uma por arquivo, e compartilham `CrudMixin`. `Foto` e `Notificacao` são mantidas porque as tabelas e o seed de demonstração as referenciam, embora não tenham fluxo exposto na API. Os repositories atuais são `TrilhaRepository`, `EventoRepository`, `CheckpointRepository`, `RelatorioRepository` e `ChecklistRepository`; alguns ainda usam ORM para consultas filtradas e não procedures.
