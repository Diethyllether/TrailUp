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

A consulta utiliza `JOIN` entre `favorito`, `trilha` e `avaliacao`, retornando os dados da trilha e sua média de avaliação.

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

A consulta combina `usuario`, `historicoTrilha`, `favorito` e `avaliacao`.

### 4. Ranking de usuários

Rota:

```http
GET /api/relatorios/usuarios/ranking?limite=10
```

Ordena os usuários pela quantidade de trilhas concluídas e avaliações realizadas.

O limite deve estar entre 1 e 100.

## Arquivos criados

```text
backend/controllers/relatorio_controller.py
backend/services/relatorio_service.py
backend/repositories/relatorio_repository.py
backend/database/procedures_relatorios.sql
```

O arquivo `backend/app.py` também foi atualizado para registrar o novo Blueprint.

## Procedures criadas

O arquivo `database/procedures_relatorios.sql` contém:

```text
sp_trilhas_por_dificuldade
sp_resumo_usuario
sp_ranking_usuarios
```

Para criar as procedures no MySQL:

```bash
mysql -u root -p trailup < database/procedures_relatorios.sql
```

Também é possível copiar e executar o conteúdo do arquivo no MySQL Workbench.

## Execução da API

```bash
cd backend
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

No Linux ou macOS:

```bash
source venv/bin/activate
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
