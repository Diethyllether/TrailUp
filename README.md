# TrailUp

> App social de trilhas para encontrar rotas, organizar expedições, participar de grupos e registrar experiências com segurança.

O projeto é dividido em uma API REST em **Flask** e um aplicativo mobile em **Flutter**, com persistência em **MySQL**.

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python + Flask |
| ORM | Flask-SQLAlchemy |
| Banco de Dados | MySQL + PyMySQL |
| Frontend | Dart + Flutter |

## Arquitetura do backend

O backend segue a separação:

```text
Controller -> Service -> Repository -> Model -> Banco de Dados
```

Estrutura principal:

```text
TrailUp/
├── backend/
│   ├── controllers/
│   ├── database/
│   │   ├── create_database.sql
│   │   └── procedures_relatorios.sql
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── tests/
│   ├── utils/
│   ├── app.py
│   ├── config.py
│   ├── init_db.py
│   └── requirements.txt
├── frontend/
└── README.md
```

## Entidades do backend

O SQLAlchemy registra 15 models:

- Usuario
- Trilha
- Avaliacao
- Favorito
- Checkpoint
- Foto
- MapaOffline
- Evento
- EventoTrilha
- ParticipanteEvento
- Notificacao
- Denuncia
- HistoricoTrilha
- RegistroRealizado
- FotoRegistro

## Funcionalidades principais

- cadastro, login e edição de perfil;
- busca e filtro de trilhas;
- CRUD de trilhas;
- avaliações e comentários;
- favoritos;
- checkpoints e fotos;
- mapas offline;
- criação e participação em eventos;
- denúncias;
- notificações;
- histórico de trilhas e registros GPS;
- relatórios com `JOIN`, `GROUP BY`, `ORDER BY`, médias e contagens;
- ranking de usuários;
- Stored Procedures no MySQL.

## Como executar

### Pré-requisitos

- MySQL
- Python 3.10+
- Flutter SDK

### 1. Banco de dados

Entre na pasta do backend:

```bash
cd backend
```

Crie o banco `trilhas_db` e todas as tabelas:

```bash
mysql -u root -p < database/create_database.sql
```

Para instalar também as Stored Procedures dos relatórios:

```bash
mysql -u root -p < database/procedures_relatorios.sql
```

### 2. Backend

Crie e ative o ambiente virtual.

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
$env:DATABASE_URL = "mysql+pymysql://root:SUASENHA@localhost:3306/trilhas_db"
$env:SECRET_KEY = "troque-esta-chave-em-producao"
python app.py
```

Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="mysql+pymysql://root:SUASENHA@localhost:3306/trilhas_db"
export SECRET_KEY="troque-esta-chave-em-producao"
python app.py
```

A API ficará disponível em:

```text
http://localhost:5000
```

Health check:

```text
GET http://localhost:5000/api/health
```

Resposta esperada:

```json
{"status":"ok","service":"TrailUp API"}
```

### 3. Teste automatizado do backend

O smoke test usa SQLite em memória e não precisa de MySQL:

```bash
python tests/smoke_test.py
```

Ele percorre os principais fluxos da API e também valida os relatórios e regras de autorização.

### 4. Frontend

Em outro terminal:

```bash
cd frontend
flutter pub get
flutter run
```

A URL da API pode ser configurada em:

```text
frontend/lib/core/config/api_config.dart
```

Sugestões:

| Ambiente | URL |
|---|---|
| Emulador Android | `http://10.0.2.2:5000/api` |
| iOS/Web/Desktop | `http://127.0.0.1:5000/api` |
| Dispositivo físico | `http://SEU_IP_LOCAL:5000/api` |

## Relatórios de banco de dados

O backend possui rotas específicas para demonstrar funcionalidades além do CRUD:

```http
GET /api/relatorios/trilhas
GET /api/relatorios/usuarios/<id>/favoritos
GET /api/relatorios/usuarios/<id>/resumo
GET /api/relatorios/usuarios/ranking
```

Mais detalhes em:

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
