# Implementação de funcionalidades que acessam o banco de dados

Esta entrega adiciona funcionalidades além do CRUD básico, mantendo a arquitetura:

`Controller -> Service -> Repository -> Model/Banco de Dados`

## Funcionalidades implementadas

### 1. Relatório de trilhas com filtros, JOIN, GROUP BY e ORDER BY

Rota:

```http
GET /api/relatorios/trilhas
```

Parâmetros opcionais:

- `dificuldade`: FACIL, MODERADA ou DIFICIL
- `localizacao`: trecho da localização
- `ordem`: `nota`, `distancia` ou `nome`

Exemplo:

```http
GET /api/relatorios/trilhas?dificuldade=FACIL&ordem=nota
```

A consulta combina as tabelas `trilha` e `avaliacao`, calcula a média das notas e conta a quantidade de avaliações.

### 2. Relatório detalhado de favoritos de um usuário

Rota protegida:

```http
GET /api/relatorios/usuarios/<id_usuario>/favoritos
```

A consulta utiliza `JOIN` entre `favorito`, `trilha` e `avaliacao`, retornando os dados da trilha e sua média de avaliação. O usuário autenticado só pode consultar os próprios favoritos.

Header obrigatório:

```http
Authorization: Bearer <token>
```

### 3. Resumo de atividade do usuário

Rota protegida:

```http
GET /api/relatorios/usuarios/<id_usuario>/resumo
```

Retorna:

- quantidade de trilhas realizadas;
- total de favoritos;
- total de avaliações;
- média das notas dadas.

A consulta combina `usuario`, `historicoTrilha`, `favorito` e `avaliacao`. O usuário autenticado só pode consultar o próprio resumo.

### 4. Ranking de usuários

Rota:

```http
GET /api/relatorios/usuarios/ranking?limite=10
```

Ordena os usuários pela quantidade de trilhas concluídas e avaliações realizadas.

O limite deve estar entre 1 e 100.

## Arquivos principais

```text
backend/controllers/relatorio_controller.py
backend/services/relatorio_service.py
backend/repositories/relatorio_repository.py
backend/database/create_database.sql
backend/database/procedures_relatorios.sql
```

O arquivo `backend/app.py` registra o Blueprint dos relatórios.

## Banco de dados e procedures

O schema principal usa o banco `trilhas_db`.

Crie o banco e as tabelas:

```bash
mysql -u root -p < database/create_database.sql
```

Depois crie as procedures:

```bash
mysql -u root -p < database/procedures_relatorios.sql
```

As procedures disponíveis são:

```text
sp_trilhas_por_dificuldade
sp_resumo_usuario
sp_ranking_usuarios
```

Também é possível executar os dois arquivos pelo MySQL Workbench.

## Execução da API

```bash
cd backend
python -m venv venv
```

No Windows:

```powershell
venv\Scripts\activate
$env:DATABASE_URL = "mysql+pymysql://root:SUASENHA@localhost:3306/trilhas_db"
$env:SECRET_KEY = "troque-esta-chave-em-producao"
```

No Linux ou macOS:

```bash
source venv/bin/activate
export DATABASE_URL="mysql+pymysql://root:SUASENHA@localhost:3306/trilhas_db"
export SECRET_KEY="troque-esta-chave-em-producao"
```

Depois:

```bash
pip install -r requirements.txt
python app.py
```

A API ficará disponível em:

```text
http://localhost:5000
```

Teste de funcionamento:

```http
GET http://localhost:5000/api/health
```

## Teste automatizado

O smoke test usa SQLite em memória e cobre os fluxos principais, incluindo os relatórios:

```bash
python tests/smoke_test.py
```

## Exemplos com curl

```bash
curl "http://localhost:5000/api/relatorios/trilhas?ordem=nota"
```

```bash
curl "http://localhost:5000/api/relatorios/usuarios/ranking?limite=5"
```

Para uma rota protegida:

```bash
curl -H "Authorization: Bearer SEU_TOKEN" \
  "http://localhost:5000/api/relatorios/usuarios/1/resumo"
```
