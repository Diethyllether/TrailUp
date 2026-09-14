# TrailUp — Backend + Site Web

O TrailUp é servido pelo próprio Flask como um **site Jinja2**, mantendo também a API REST existente. A persistência usa **Flask-SQLAlchemy + MySQL** e os mapas do site usam **Google Maps JavaScript API**.

## Arquitetura

Fluxo das páginas web:

```text
Jinja2/HTML -> WebController -> Service -> Model/Repository -> Banco de Dados
```

Fluxo da API JSON:

```text
Cliente -> Controller API -> Service -> Model/Repository -> Banco de Dados
```

A regra de negócio permanece no backend. Os templates não executam consultas diretamente no banco.

Estrutura principal:

```text
backend/
├── app.py
├── config.py
├── extensions.py
├── controllers/
│   └── web_controller.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── map.html
│   ├── trail_detail.html
│   ├── events.html
│   ├── favorites.html
│   ├── login.html
│   ├── register.html
│   └── profile.html
├── static/
│   └── css/site.css
├── database/
│   ├── create_database.sql
│   └── procedures_relatorios.sql
├── models/
├── repositories/
├── services/
├── tests/
└── utils/
```

## Dependências Python

```text
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
PyMySQL==1.1.1
```

Jinja2 já é uma dependência do Flask, portanto não precisa ser adicionado separadamente ao `requirements.txt`.

## Banco de dados

Banco padrão:

```text
trilhas_db
```

O projeto considera `database/create_database.sql` como a **fonte única do schema atual**. Não há suporte a migração automática de bancos antigos: para desenvolvimento, crie um banco novo usando o script atual.

Criação do banco:

```bash
mysql -u root -p < database/create_database.sql
```

Stored Procedures:

```bash
mysql -u root -p < database/procedures_relatorios.sql
```

Para popular o banco com dados de demonstração:

```bash
python seed_demo.py
```

A funcionalidade de mapas offline foi removida. A rota exibida no Google Maps é formada pelos checkpoints GPS associados a cada trilha.

## Site Jinja2

Rotas principais:

| Rota | Função |
|---|---|
| `/` | início, busca e filtros de trilhas |
| `/mapa` | mapa de expedições no Google Maps |
| `/login` | login web |
| `/cadastro` | cadastro web |
| `/trilhas/<id>` | detalhes + rota da trilha no Google Maps |
| `/favoritos` | trilhas favoritas |
| `/eventos` | listar e criar expedições |
| `/perfil` | perfil básico |

A autenticação das páginas usa a sessão assinada do Flask. A API REST continua usando `Authorization: Bearer <token>`.

## Google Maps

Configure:

```text
GOOGLE_MAPS_API_KEY
```

A chave é utilizada somente pelo frontend Jinja2 para carregar a Google Maps JavaScript API.

Na página de uma trilha:

1. o backend busca os checkpoints da trilha;
2. remove coordenadas inválidas e `0,0`;
3. o template recebe os pontos como JSON;
4. JavaScript cria uma `google.maps.Polyline`;
5. o primeiro e o último checkpoint recebem marcadores de início/fim.

Na página `/mapa`, os eventos com latitude/longitude são mostrados como marcadores.

Em produção, restrinja a API Key ao domínio do TrailUp no Google Cloud Console.

## Executando

### Windows PowerShell

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
$env:DATABASE_URL = "mysql+pymysql://root:SUASENHA@localhost:3306/trilhas_db"
$env:SECRET_KEY = "troque-esta-chave-em-producao"
$env:GOOGLE_MAPS_API_KEY = "SUA_CHAVE"
python app.py
```

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="mysql+pymysql://root:SUASENHA@localhost:3306/trilhas_db"
export SECRET_KEY="troque-esta-chave-em-producao"
export GOOGLE_MAPS_API_KEY="SUA_CHAVE"
python app.py
```

Site:

```text
http://localhost:5000/
```

Health check:

```http
GET /api/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "TrailUp API + Web"
}
```

## Endpoints principais da API

Todas as rotas abaixo usam `/api`.

| Recurso | Método/Rota |
|---|---|
| Usuário | `POST /usuarios` |
| Usuário | `GET /usuarios/<id>` |
| Usuário | `PUT /usuarios/<id>` |
| Autenticação | `POST /login` |
| Trilha | `GET /trilhas` |
| Trilha | `GET /trilhas/<id>` |
| Trilha | `POST /trilhas` |
| Avaliação | `GET/POST /trilhas/<id>/avaliacoes` |
| Favorito | `GET /usuarios/<id>/favoritos` |
| Favorito | `POST /favoritos` |
| Favorito | `DELETE /favoritos/<idTrilha>` |
| Checkpoint | `GET/POST /trilhas/<id>/checkpoints` |
| Foto | `GET/POST /trilhas/<id>/fotos` |
| Evento | `GET/POST /eventos` |
| Evento | `GET/PUT/DELETE /eventos/<id>` |
| Evento | `POST /eventos/<id>/entrar` |
| Evento | `POST /eventos/<id>/sair` |
| Denúncia | `GET/POST /eventos/<id>/denuncias` |
| Notificação | `GET /usuarios/<id>/notificacoes` |
| Histórico | `GET /usuarios/<id>/historico` |
| Histórico | `POST /historico` |
| Relatórios | `GET /relatorios/trilhas` |
| Relatórios | `GET /relatorios/usuarios/<id>/resumo` |
| Ranking | `GET /relatorios/usuarios/ranking` |

## Testes

```bash
python tests/smoke_test.py
python tests/requisitos_busca_test.py
```

## Variáveis de ambiente

| Variável | Função |
|---|---|
| `DATABASE_URL` | conexão com o banco |
| `SECRET_KEY` | sessão Flask e assinatura de tokens |
| `TOKEN_EXP_MINUTES` | validade do token da API |
| `GOOGLE_MAPS_API_KEY` | Google Maps JavaScript API |
| `FLASK_DEBUG` | modo debug |

O projeto não carrega `.env` automaticamente; exporte as variáveis no ambiente antes de executar.
