# TrailUp — Backend

API REST do TrailUp construída com **Flask**, **Flask-SQLAlchemy** e **MySQL**.

## Arquitetura

O backend segue o fluxo:

```text
Controller -> Service -> Repository -> Model -> Banco de Dados
```

- **Controller:** recebe a requisição HTTP e monta a resposta.
- **Service:** aplica validações e regras de negócio.
- **Repository:** executa consultas e operações de persistência.
- **Model:** representa as tabelas do banco com SQLAlchemy.

Estrutura:

```text
backend/
├── app.py
├── config.py
├── extensions.py
├── init_db.py
├── requirements.txt
├── .env.example
├── controllers/
├── database/
│   ├── create_database.sql
│   └── procedures_relatorios.sql
├── models/
├── repositories/
├── services/
├── tests/
└── utils/
```

## Dependências

```text
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
PyMySQL==1.1.1
```

## Banco de dados

O banco padrão do projeto é:

```text
trilhas_db
```

A configuração padrão está em `config.py`:

```text
mysql+pymysql://root:@localhost:3306/trilhas_db
```

É recomendado definir `DATABASE_URL` no ambiente com a senha correta do seu MySQL.

### Criar banco e tabelas

Na pasta `backend`:

```bash
mysql -u root -p < database/create_database.sql
```

O arquivo cria as tabelas correspondentes aos 15 models registrados pelo backend.

### Criar as Stored Procedures

```bash
mysql -u root -p < database/procedures_relatorios.sql
```

Procedures disponíveis:

```text
sp_trilhas_por_dificuldade
sp_resumo_usuario
sp_ranking_usuarios
```

### Atualizar tabelas em desenvolvimento

Caso uma nova tabela seja adicionada aos models:

```bash
python init_db.py
```

`db.create_all()` cria estruturas ausentes, mas não substitui um sistema de migrations para alterações complexas em colunas existentes.

## Models

Os models registrados são:

1. Usuario
2. Trilha
3. Avaliacao
4. Favorito
5. Checkpoint
6. Foto
7. MapaOffline
8. Evento
9. EventoTrilha
10. ParticipanteEvento
11. Notificacao
12. Denuncia
13. HistoricoTrilha
14. RegistroRealizado
15. FotoRegistro

## Executando a API

### Windows PowerShell

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
$env:DATABASE_URL = "mysql+pymysql://root:SUASENHA@localhost:3306/trilhas_db"
$env:SECRET_KEY = "troque-esta-chave-em-producao"
python app.py
```

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="mysql+pymysql://root:SUASENHA@localhost:3306/trilhas_db"
export SECRET_KEY="troque-esta-chave-em-producao"
python app.py
```

Servidor:

```text
http://localhost:5000
```

Health check:

```http
GET /api/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "TrailUp API"
}
```

## Autenticação

O login retorna um token assinado. Rotas protegidas exigem:

```http
Authorization: Bearer <token>
```

O tempo padrão de validade é de 1440 minutos e pode ser alterado com `TOKEN_EXP_MINUTES`.

## Endpoints principais

Todas as rotas abaixo usam o prefixo `/api`.

| Recurso | Método/Rota | Função |
|---|---|---|
| Usuário | `POST /usuarios` | cadastrar usuário |
| Usuário | `GET /usuarios` | listar usuários |
| Usuário | `GET /usuarios/<id>` | buscar usuário |
| Usuário | `PUT /usuarios/<id>` | editar o próprio perfil |
| Usuário | `DELETE /usuarios/<id>` | excluir o próprio perfil |
| Autenticação | `POST /login` | realizar login |
| Autenticação | `POST /recuperar-senha` | solicitar recuperação |
| Autenticação | `POST /redefinir-senha` | redefinir senha |
| Trilha | `GET /trilhas` | listar, buscar e filtrar |
| Trilha | `GET /trilhas/<id>` | buscar trilha |
| Trilha | `POST /trilhas` | criar trilha |
| Trilha | `PUT /trilhas/<id>` | editar trilha |
| Trilha | `DELETE /trilhas/<id>` | excluir trilha |
| Avaliação | `GET /trilhas/<id>/avaliacoes` | listar avaliações |
| Avaliação | `POST /trilhas/<id>/avaliacoes` | criar avaliação |
| Avaliação | `PUT /avaliacoes/<id>` | editar a própria avaliação |
| Avaliação | `DELETE /avaliacoes/<id>` | excluir a própria avaliação |
| Favorito | `GET /usuarios/<id>/favoritos` | listar favoritos |
| Favorito | `POST /favoritos` | favoritar trilha |
| Favorito | `DELETE /favoritos/<idTrilha>` | remover favorito |
| Checkpoint | `GET/POST /trilhas/<id>/checkpoints` | listar/criar checkpoints |
| Checkpoint | `DELETE /checkpoints/<id>` | excluir checkpoint |
| Foto | `GET/POST /trilhas/<id>/fotos` | listar/criar fotos |
| Foto | `DELETE /fotos/<id>` | excluir foto |
| Mapa Offline | `GET/POST /trilhas/<id>/mapas-offline` | listar/criar mapas |
| Mapa Offline | `DELETE /mapas-offline/<id>` | excluir mapa |
| Evento | `GET/POST /eventos` | listar/criar eventos |
| Evento | `GET/PUT/DELETE /eventos/<id>` | consultar/editar/excluir evento |
| Evento | `POST /eventos/<id>/entrar` | entrar no evento |
| Evento | `POST /eventos/<id>/sair` | sair do evento |
| Evento | `GET /eventos/<id>/participantes` | listar participantes |
| Denúncia | `GET/POST /eventos/<id>/denuncias` | listar/criar denúncias |
| Denúncia | `PUT /denuncias/<id>/status` | atualizar status |
| Notificação | `GET /usuarios/<id>/notificacoes` | listar notificações |
| Notificação | `POST /notificacoes` | criar notificação |
| Notificação | `PUT /notificacoes/<id>/lida` | marcar como lida |
| Histórico | `GET /usuarios/<id>/historico` | listar histórico |
| Histórico | `POST /historico` | registrar trilha realizada |
| Histórico | `GET/POST /historico/<id>/registros` | registros GPS |
| Histórico | `GET/POST /registros/<id>/fotos` | fotos do registro |

## Relatórios e funcionalidades de banco

### Trilhas com agregações

```http
GET /api/relatorios/trilhas
```

Parâmetros:

- `dificuldade`
- `localizacao`
- `ordem=nota|distancia|nome`

A consulta usa `LEFT JOIN`, `GROUP BY`, `ORDER BY`, `AVG` e `COUNT`.

### Favoritos detalhados

```http
GET /api/relatorios/usuarios/<id>/favoritos
```

Rota autenticada. O usuário só pode acessar os próprios favoritos.

### Resumo de atividade

```http
GET /api/relatorios/usuarios/<id>/resumo
```

Rota autenticada. Retorna trilhas realizadas, favoritos, avaliações e média das notas do próprio usuário.

### Ranking

```http
GET /api/relatorios/usuarios/ranking?limite=10
```

O limite aceito é de 1 a 100.

Mais detalhes em `ATIVIDADE_FUNCIONALIDADES_BANCO.md`.

## Testes

O teste principal usa SQLite em memória, portanto não depende de um servidor MySQL para validar a lógica da API:

```bash
python tests/smoke_test.py
```

O teste percorre cadastro, login, autorização, CRUDs principais, favoritos, avaliações, checkpoints, fotos, mapas offline, eventos, denúncias, notificações, histórico, relatórios, ranking, recuperação de senha e health check.

## Variáveis de ambiente

| Variável | Exemplo | Função |
|---|---|---|
| `DATABASE_URL` | `mysql+pymysql://root:senha@localhost:3306/trilhas_db` | conexão MySQL |
| `SECRET_KEY` | `uma-chave-secreta` | assinatura dos tokens |
| `TOKEN_EXP_MINUTES` | `1440` | validade do token |
| `FLASK_DEBUG` | `false` | modo debug |

O arquivo `.env.example` é apenas uma referência. O projeto não carrega `.env` automaticamente; as variáveis devem ser definidas no ambiente antes de executar a API.
