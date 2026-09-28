# TrailUp

> Plataforma web social de trilhas para encontrar rotas, organizar expedições, participar de grupos e registrar experiências.

O TrailUp foi migrado do aplicativo Flutter para um **site Flask + Jinja2** em arquitetura MVC. A persistência permanece em **MySQL** e os mapas das trilhas são exibidos online com **Google Maps JavaScript API**.

A antiga funcionalidade de **download de mapas offline foi descontinuada**. O site usa os checkpoints GPS já cadastrados para desenhar a rota diretamente no Google Maps, sem salvar pacotes de tiles no dispositivo.

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python + Flask |
| Frontend web | Jinja2 + HTML + CSS + JavaScript |
| Mapas | Google Maps JavaScript API |
| ORM | Flask-SQLAlchemy |
| Banco de Dados | MySQL + PyMySQL |

## Arquitetura

As regras de negócio continuam centralizadas no backend:

```text
Página Jinja2 -> Controller Flask -> Service -> Model/Repository -> MySQL
```

Responsabilidades das camadas:

- **View:** templates Jinja2 e arquivos estáticos; apenas apresentam dados.
- **Controller:** traduz HTTP/formulários para chamadas de casos de uso e respostas.
- **Service:** concentra validações, regras de negócio e orquestração.
- **Repository:** é a única camada que consulta ou persiste com SQLAlchemy.
- **Model:** representa as entidades e o mapeamento objeto-relacional.

Os Services e Controllers aceitam suas dependências por construtor. Isso reduz
acoplamento, permite substituir implementações e mantém cada classe com uma
responsabilidade principal, em conformidade com os princípios SOLID.

O frontend web reutiliza os mesmos Services e Models da aplicação, evitando duplicar regras de negócio no JavaScript.

The web frontend is organized under `frontend/`: templates are in
`frontend/templates`, styles in `frontend/static/css`, and JavaScript in
`frontend/static/js`. Flask serves the static assets at `/static`.

Estrutura principal:

```text
TrailUp/
├── backend/
│   ├── controllers/
│   │   └── web_controller.py
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── static/
│   │   └── css/site.css
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── trail_detail.html
│   │   ├── events.html
│   │   ├── favorites.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── app.py
│   ├── config.py
│   └── requirements.txt
├── frontend/              # Flutter legado/descontinuado
└── README.md
```

## Funcionalidades web

1. Cadastro de usuário
2. Login e sessão no navegador
3. Busca de trilhas por nome/localização
4. Filtro por dificuldade
5. Visualização de detalhes da trilha
6. Visualização da rota e checkpoints no Google Maps
7. Adicionar e remover trilhas dos favoritos
8. Listar favoritos do usuário
9. Listar e criar eventos/expedições
10. Participar de eventos/expedições
11. Perfil básico do usuário

Os recursos do backend são acessados pelas páginas MVC por meio do `WebController` e da camada de services.

## Google Maps

A página de detalhes da trilha transforma os checkpoints armazenados no banco em uma `Polyline` do Google Maps. O primeiro ponto recebe o marcador de início e o último recebe o marcador de fim.

Para habilitar o mapa:

1. Crie um projeto no Google Cloud.
2. Ative **Maps JavaScript API**.
3. Crie uma API Key.
4. Em produção, restrinja a chave ao domínio do TrailUp.
5. Exporte a variável `GOOGLE_MAPS_API_KEY` antes de iniciar o Flask.

Exemplo no PowerShell:

```powershell
$env:GOOGLE_MAPS_API_KEY = "SUA_CHAVE"
```

Linux/macOS:

```bash
export GOOGLE_MAPS_API_KEY="SUA_CHAVE"
```

Se a chave não estiver configurada, a página continua funcionando e informa que o mapa precisa ser configurado.

## Mapas offline

O recurso foi removido da aplicação ativa após a migração para web. Não há mais botão de download de mapa nem rota `/api` registrada para mapas offline. O modelo/tabela legado pode permanecer no banco durante a transição para não exigir uma migração destrutiva imediata, mas não faz parte do fluxo atual do site.

## Como executar

### Pré-requisitos

- Python 3.10+
- MySQL
- Chave da Google Maps JavaScript API para exibir mapas

### 1. Banco de dados

```bash
cd backend
mysql -u root -p < database/create_database.sql
```

Para instalar também as Stored Procedures dos relatórios:

```bash
mysql -u root -p < database/procedures_relatorios.sql
```

### 2. Ambiente Python

Windows PowerShell:

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
$env:DATABASE_URL = "mysql+pymysql://root:SUASENHA@localhost:3306/trilhas_db"
$env:SECRET_KEY = "troque-esta-chave-em-producao"
$env:GOOGLE_MAPS_API_KEY = "SUA_CHAVE"
python app.py
```

Linux/macOS:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="mysql+pymysql://root:SUASENHA@localhost:3306/trilhas_db"
export SECRET_KEY="troque-esta-chave-em-producao"
export GOOGLE_MAPS_API_KEY="SUA_CHAVE"
python app.py
```

Abra:

```text
http://localhost:5000/
```

Health check da API:

```text
GET http://localhost:5000/api/health
```

Resposta esperada:

```json
{"status":"ok","service":"TrailUp API + Web"}
```

## Frontend web e Flutter legado

O site Jinja2 está em `frontend/templates`, com CSS e JavaScript em
`frontend/static`. O aplicativo Flutter legado permanece em `frontend/lib`;
o produto web é executado pelo Flask em `http://localhost:5000/`.

## Relatórios de banco de dados

```http
GET /api/relatorios/trilhas
GET /api/relatorios/usuarios/<id>/favoritos
GET /api/relatorios/usuarios/<id>/resumo
GET /api/relatorios/usuarios/ranking
```

Mais detalhes:

- `backend/ATIVIDADE_FUNCIONALIDADES_BANCO.md`
- `backend/README.md`

## Time

| Nome | Papel |
|---|---|
| Felipe Cornélio Leite | Front End |
| Nikolas Ansur Proti Soares | Front End |
| Lucca Freitas Leandro | Banco de Dados / Infra |
| Pedro da Silva Brum | Banco de Dados / Infra |
| Miguel Seleme de Azevedo | Back End |
| Miguel Anthony de Oliveira | Back End |
