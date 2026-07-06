# TrailUp — Backend (Flask + SQLAlchemy, MVC)

API REST para o app mobile TrailUp (Flutter). Estrutura inspirada em
[gleisonbt/projeto-flask-sqlalchemy](https://github.com/gleisonbt/projeto-flask-sqlalchemy):
**Controller → Service → Repository → Model**, com Flask puro (Blueprints) e
Flask-SQLAlchemy como ORM sobre **MySQL**.

**Dependências: `Flask`, `Flask-SQLAlchemy` e `PyMySQL`** (ver
`requirements.txt`) — o PyMySQL é o driver que o Flask-SQLAlchemy precisa
pra falar com o MySQL, não tem como rodar sobre MySQL sem ele. Fora isso,
nada de Flask-Cors, python-dotenv ou PyJWT: hash de senha e token de login
usam `werkzeug.security` e `itsdangerous` (dependências que já vêm
instaladas junto com o próprio Flask) e as datas usam o módulo `datetime`
da biblioteca padrão do Python.

```
backend/
├── app.py
├── config.py
├── extensions.py
├── init_db.py
├── requirements.txt
├── .env.example
├── database/
│   └── create_database.sql
├── models/
├── repositories/
├── services/
├── controllers/
└── utils/
    └── auth.py
```

Fluxo de uma requisição: `controller` recebe o JSON → chama o `service`
correspondente → o `service` valida regras de negócio e usa o `repository`
→ o `repository` conversa com o `model`/banco. Erros de validação viram
`ValueError` (→ 400/404) ou `PermissionError` (→ 403), tratados no controller.

## Ajustes feitos em cima do material enviado

Comparando `create_database.sql` com a lista de 20 requisitos e o diagrama ER
em PDF, encontrei e corrigi:

1. **Faltava a tabela `favorito`** (requisito 14) — criada como associativa
   N:N entre `usuario` e `trilha`, com `UNIQUE(idUsuario, idTrilha)`.
2. **`evento` não tinha coordenadas** — como a descrição do produto fala em
   "salas" aparecendo como *pins* em tempo real no mapa, adicionei
   `latitude`, `longitude`, `horarioSaida` e `imediata`.
3. **`mapaOffline` não guardava o arquivo em si** — adicionei `arquivoUrl`.
4. **`notificacao` e `denuncia`** apontavam só para `evento`; adicionei o
   vínculo direto com `usuario` (destinatário da notificação, denunciante e
   denunciado), já que "enviar notificação ao usuário" e "denunciar
   comportamento" exigem saber *quem*.
5. **`historicoTrilha` não tinha `idUsuario`** — histórico é por pessoa, não
   só por evento/trilha.
6. **`trilha`** ganhou `imagemUrl` (req. 7) e `tempoEstimadoMin`, calculado
   automaticamente pelo backend (req. 15).

O backend roda sobre MySQL, usando `database/create_database.sql` como
fonte da verdade do schema (é ele que você roda no MySQL antes de subir a
API — `app.py` não cria tabela nenhuma sozinho). O único pacote externo
além do Flask e do Flask-SQLAlchemy é o `PyMySQL` (driver obrigatório);
autenticação usa `werkzeug.security`/`itsdangerous`, que já vêm com o
Flask, e datas usam o `datetime` da biblioteca padrão.

O diagrama ER em PDF (grupo Lucca Freitas et al.) modela o mesmo domínio de
forma mais simplificada (sem `checkpoint`/`foto`/`denuncia` como tabelas
próprias) — não usei esse schema diretamente porque diverge do
`create_database.sql` já em uso no projeto, mas o fato de ele já ter uma
entidade `FAVORITO` reforça que a ausência dela no `create_database.sql`
era mesmo uma lacuna.

`CHECKLIST_ITEM` do PDF não entrou porque não está entre os 20 requisitos
do `lista_requisitos.txt` — se quiser esse recurso (checklist de
equipamentos por trilha) eu adiciono depois.

## Rodando localmente

Pré-requisito: um servidor MySQL rodando e acessível.

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

mysql -u root -p < database/create_database.sql

cp .env.example .env
python app.py
```

Se editar um model depois (novo campo, nova tabela) e quiser aplicar sem
mexer no `.sql` na mão, rode `python init_db.py` — ele usa
`db.create_all()`, que cria só o que estiver faltando (não apaga dados).

Sanity check ponta a ponta sem precisar de MySQL rodando (usa SQLite em
memória, só pra validar a lógica dos controllers/services): `python
tests/smoke_test.py`.

## Autenticação

Login devolve um token assinado (`utils/auth.py`, via `itsdangerous` — a
mesma lib que o Flask usa para assinar cookies de sessão, expira em 24h por
padrão). Rotas protegidas exigem o header:

```
Authorization: Bearer <token>
```

## Endpoints (prefixo `/api`)

| Requisito | Método/Rota | Descrição |
|---|---|---|
| 1 | `POST /usuarios` | cadastro |
| 2 | `POST /login` | login → `{token, usuario}` |
| 3 | `POST /recuperar-senha` → `POST /redefinir-senha` | recuperação de senha |
| 4 | `GET/PUT/DELETE /usuarios/<id>` | perfil |
| 5,6,8 | `GET /trilhas?nome=&localizacao=&dificuldade=` | busca e filtro |
| 7 | `GET/POST/DELETE /trilhas/<id>/fotos`, `/fotos/<id>` | imagens da trilha |
| 9 | `GET/POST/DELETE /trilhas/<id>/checkpoints`, `/checkpoints/<id>` | pontos no mapa da trilha |
| 10 | `GET/POST/DELETE /trilhas/<id>/mapas-offline`, `/mapas-offline/<id>` | mapas offline |
| 11 | *(client-side, geolocalização do device)* |
| 12 | `GET/POST/PUT/DELETE /trilhas/<id>/avaliacoes`, `/avaliacoes/<id>` | notas e comentários |
| 13 | `GET/POST /eventos/<id>/denuncias`, `PUT /denuncias/<id>/status` | denúncias + moderação |
| 14 | `GET /usuarios/<id>/favoritos`, `POST /favoritos`, `DELETE /favoritos/<idTrilha>` | favoritos |
| 15 | *(automático)* — `tempoEstimadoMin` calculado ao criar/editar trilha |
| 16 | `GET/POST /historico/<id>/registros`, `/registros/<id>/fotos` | checkpoints via GPS + fotos |
| 17 | `GET/POST/PUT/DELETE /eventos`, `/eventos/<id>`, `.../entrar`, `.../sair` | salas/eventos |
| 18 | `GET /usuarios/<id>/historico`, `POST /historico` | histórico de trilhas |
| 19 | `GET /usuarios/<id>/notificacoes`, `POST /notificacoes`, `PUT /notificacoes/<id>/lida` | notificações |
| 20 | *(client-side — cache local no Flutter)* |

`GET /eventos?mapa=true` retorna só as salas com coordenadas definidas, para
plotar como pins em tempo real (é o comportamento descrito no `descricao.txt`).

`GET /api/health` para checar se a API está no ar.

## Próximos passos sugeridos

- Trocar o dicionário em memória de tokens de recuperação de senha por uma
  tabela (ou Redis) antes de ir para produção — hoje ele reseta ao reiniciar
  o servidor.
- SOS com GPS e check-in automático de fim de trilha (mencionados na
  descrição do produto) ainda não têm endpoint próprio — dá pra modelar como
  um tipo de `notificacao`/`denuncia` de prioridade alta, ou uma tabela nova
  `alertaSOS`, se quiser que eu implemente.
- Se o schema for evoluir com frequência, vale considerar Flask-Migrate
  (Alembic) no lugar de editar o `create_database.sql`/`init_db.py` na mão,
  pra não ter que recriar tabelas manualmente a cada mudança de model.
