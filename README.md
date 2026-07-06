# TrailUp

> App social de trilhas onde a experiência coletiva é o centro — com estrutura, segurança e sustentabilidade para crescer além do entusiasmo inicial.

Usuários criam **expedições** em tempo real, encontram grupos para trilhar juntos, registram checkpoints com fotos georreferenciadas e contam com recursos de segurança integrados — como botão SOS com GPS e check-in automático ao fim da trilha.

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python + Flask |
| Frontend | Dart + Flutter |
| Banco de Dados | MySQL |

---

## Time

| Nome | Papel |
|---|---|
| Felipe Cornélio Leite | Front End |
| Nikolas Ansur Proti Soares| Front End |
| Lucca Freitas Leandro | Banco de Dados/Infra |
| Pedro da Silva Brum | Banco de Dados/Infra |
| Miguel Seleme de Azevedo | Back End|
| Miguel Anthony de Oliveira| Back End |

---

## Como executar

O projeto é dividido em duas partes: a **API Flask** em `backend/` e o **app Flutter** em `frontend/`. Para usar o app com dados reais, suba primeiro o servidor e depois o cliente mobile.

### Pré-requisitos

- **MySQL** — servidor rodando e acessível
- **Python 3.10+** — para a API
- **Flutter SDK** — para o app ([instalação](https://docs.flutter.dev/get-started/install))
- Emulador Android/iOS ou dispositivo físico configurado (`flutter doctor`)

### 1. Servidor (backend)

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Crie o banco e as tabelas (ajuste usuário/senha conforme seu MySQL):

```powershell
mysql -u root -p < database\create_database.sql
```

Configure a conexão com o banco. O projeto não usa `python-dotenv`; defina as variáveis no terminal antes de subir a API (veja `backend/.env.example` como referência):

```powershell
$env:DATABASE_URL = "mysql+pymysql://root:SUASENHA@localhost:3306/trilhas_db"
$env:SECRET_KEY = "troque-esta-chave-em-producao"
python app.py
```

A API sobe em **http://localhost:5000**. Confirme com:

```powershell
curl http://localhost:5000/api/health
```

Resposta esperada: `{"status":"ok","service":"TrailUp API"}`.

> **Linux/macOS:** use `source venv/bin/activate` e `export DATABASE_URL=...` no lugar dos comandos PowerShell acima.

Se alterar os models depois do schema inicial, rode `python init_db.py` para criar tabelas/colunas faltantes sem apagar dados existentes.

### 2. Aplicativo (frontend)

Em outro terminal:

```powershell
cd frontend
flutter pub get
flutter run
```

Antes de rodar contra a API local, ajuste a URL base em `frontend/lib/core/config/api_config.dart`:

| Ambiente | `baseUrl` sugerida |
|---|---|
| Emulador Android | `http://10.0.2.2:5000/api` |
| Simulador iOS / Web / Desktop | `http://127.0.0.1:5000/api` |
| Dispositivo físico (mesma rede Wi‑Fi) | `http://SEU_IP_LOCAL:5000/api` |

O backend escuta em `0.0.0.0:5000`, então dispositivos na mesma rede conseguem acessá-lo pelo IP da máquina onde a API está rodando.

### Ordem recomendada

1. Subir o MySQL e aplicar `backend/database/create_database.sql`
2. Iniciar a API com `python app.py` em `backend/`
3. Configurar `ApiConfig.baseUrl` no Flutter
4. Executar `flutter run` em `frontend/`

Documentação detalhada da API (endpoints, autenticação, estrutura MVC): [`backend/README.md`](backend/README.md).

---
