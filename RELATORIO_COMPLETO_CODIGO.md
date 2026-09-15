# Relatório Completo do Código — TrailUp

## 1. Visão geral

O TrailUp é uma plataforma web social voltada para trilhas. O sistema permite cadastrar usuários, autenticar, pesquisar trilhas, visualizar detalhes e rotas, favoritar trilhas, avaliar experiências, consultar checklist de equipamentos, criar e participar de expedições e consultar o histórico do usuário.

A aplicação ativa utiliza **Python + Flask** no servidor, **Jinja2 + HTML + CSS + JavaScript** no frontend, **Flask-SQLAlchemy** como ORM e **MySQL** como banco de dados. A versão Flutter existente na pasta `frontend/` é legada e não é o frontend principal atual.

O mapa foi migrado para **MapLibre GL JS + OpenFreeMap**. Portanto, a aplicação não precisa de chave da Google Maps API. As rotas das trilhas são construídas a partir dos checkpoints GPS armazenados no próprio banco.

---

## 2. Arquitetura geral

O projeto procura separar responsabilidades em camadas:

```text
Interface Jinja2 / Cliente REST
            ↓
      Controller Flask
            ↓
           Service
            ↓
     Model / Repository
            ↓
           MySQL
```

A ideia central é impedir que regras de negócio fiquem espalhadas pela interface. O Controller interpreta a requisição HTTP, chama um Service e prepara a resposta. O Service executa o caso de uso. Models representam as entidades persistidas e Repositories concentram consultas específicas.

Há dois tipos de interface sobre o mesmo backend:

```text
Navegador → páginas Jinja2 → WebController

Cliente/API → /api/... → Controllers REST
```

Ambos compartilham os componentes de domínio e persistência.

---

## 3. Estrutura principal

```text
TrailUp/
├── backend/
│   ├── controllers/       # Controllers web e REST
│   ├── database/          # Criação do banco e Stored Procedures
│   ├── models/            # Entidades SQLAlchemy
│   ├── repositories/      # Consultas especializadas
│   ├── services/          # Regras de negócio
│   │   └── casos_uso/     # Services de casos de uso específicos
│   ├── static/            # CSS e arquivos estáticos
│   ├── templates/         # Páginas Jinja2
│   ├── tests/             # Testes
│   ├── app.py             # Inicialização do Flask
│   ├── config.py          # Configurações
│   └── extensions.py      # Instância compartilhada do SQLAlchemy
├── frontend/              # Flutter legado
└── README.md
```

---

# 4. Inicialização da aplicação

## `backend/app.py`

É o ponto central da aplicação Flask.

A função `create_app()`:

1. cria a instância de `Flask`;
2. carrega `Config`;
3. configura `strict_slashes`;
4. inicializa o SQLAlchemy;
5. registra o frontend web;
6. registra os Blueprints da API em `/api`;
7. configura CORS;
8. registra o health check;
9. registra tratamentos de erro 404, 405 e 500.

Os Models são importados antes da inicialização completa para que o SQLAlchemy conheça as tabelas e Foreign Keys.

### Blueprints REST registrados

A aplicação possui Blueprints para:

- usuários;
- trilhas;
- avaliações;
- favoritos;
- checkpoints;
- fotos;
- eventos;
- notificações;
- denúncias;
- histórico;
- relatórios.

O `web_bp` é registrado sem `/api`, pois representa as páginas do site.

### Health check

```http
GET /api/health
```

Retorna uma resposta indicando que o backend está funcionando.

### Tratamento de erros

Quando uma URL da API falha, a resposta é JSON. Para páginas normais, o Flask renderiza templates de erro. Em erro 500 também é executado `db.session.rollback()`, evitando deixar a sessão SQLAlchemy em estado inválido.

---

# 5. Configuração

## `backend/config.py`

Centraliza as configurações lidas do ambiente.

Principais opções:

- `SQLALCHEMY_DATABASE_URI`: conexão com MySQL;
- `SQLALCHEMY_TRACK_MODIFICATIONS = False`;
- `SECRET_KEY`: usada pelo Flask e mecanismos de autenticação/sessão;
- `TOKEN_EXP_MINUTES`: validade configurável de token;
- `DEBUG`: controlado por `FLASK_DEBUG`.

O endereço padrão atual do banco é:

```text
mysql+pymysql://root:@localhost:3307/trilhas_db
```

Pode ser substituído pela variável `DATABASE_URL`.

O mapa não exige variável de API, pois utiliza MapLibre GL JS com OpenFreeMap.

---

# 6. SQLAlchemy e persistência

## `backend/extensions.py`

Mantém uma única instância:

```python
db = SQLAlchemy()
```

Ela é importada pelos Models e inicializada no `app.py`. Isso evita criar várias instâncias independentes do ORM.

---

# 7. Models

Os Models representam as tabelas do banco e herdam de `db.Model`.

## 7.1 Usuario

Representa uma conta do TrailUp.

Principais dados:

- ID;
- nome;
- e-mail;
- senha armazenada de forma protegida;
- foto de perfil;
- data de cadastro.

É a entidade central para favoritos, avaliações, expedições, histórico, notificações e denúncias.

## 7.2 Trilha

Representa uma rota de caminhada/trilha.

Armazena:

- nome;
- localização;
- distância;
- duração;
- dificuldade;
- descrição;
- imagem;
- tempo estimado.

O tempo estimado pode ser calculado pela camada de Service a partir da distância e dificuldade.

## 7.3 Checkpoint

Cada checkpoint contém uma coordenada GPS pertencente a uma trilha.

Campos importantes:

```text
latitude
longitude
horario
idTrilha
```

A sequência dos checkpoints representa o traçado da rota. O frontend transforma esses pontos em uma `LineString` GeoJSON exibida no MapLibre.

## 7.4 ChecklistItem

Representa um equipamento associado a uma trilha.

Campos:

```text
idChecklistItem
descricao
obrigatorio
idTrilha
```

Um item pode ser obrigatório ou apenas recomendado. Ao excluir uma trilha, seus itens são removidos pelo relacionamento `ON DELETE CASCADE` definido no banco.

## 7.5 Avaliacao

Relaciona usuário e trilha e registra a experiência do usuário.

Possui:

- nota de 1 a 5;
- comentário;
- data;
- usuário;
- trilha.

## 7.6 Favorito

Representa uma trilha salva por um usuário.

O banco possui restrição para impedir duplicação do mesmo par usuário/trilha.

## 7.7 Evento

Representa uma expedição.

Entre os dados estão:

- título;
- descrição;
- data;
- horário de saída;
- indicação de expedição imediata;
- quantidade de vagas;
- tipo `INDIVIDUAL` ou `GRUPO`;
- latitude e longitude;
- criador.

## 7.8 EventoTrilha

Tabela associativa entre evento e trilha. Permite vincular uma expedição a uma ou mais trilhas.

## 7.9 ParticipanteEvento

Tabela associativa que informa quais usuários participam de quais expedições.

Ela é a fonte usada para responder perguntas como:

```text
O usuário participa deste evento?
Quais eventos o usuário participa?
Quantos participantes o evento possui?
```

## 7.10 HistoricoTrilha

Registra uma trilha efetivamente realizada pelo usuário.

Contém:

- data da realização;
- tempo gasto;
- avaliação pessoal;
- usuário;
- trilha;
- evento opcional.

O vínculo opcional com evento permite registrar que uma trilha foi concluída dentro de uma expedição.

## 7.11 RegistroRealizado

Representa pontos GPS registrados durante uma realização armazenada no histórico.

## 7.12 FotoRegistro

Associa imagens aos registros de uma atividade realizada.

## 7.13 Foto

Representa imagens associadas diretamente às trilhas.

## 7.14 Notificacao

Armazena mensagens destinadas ao usuário, com data e estado de leitura. Pode ter relação com um evento.

## 7.15 Denuncia

Representa denúncias relacionadas a eventos e usuários. O banco restringe os estados possíveis, como `PENDENTE`, `EM_ANALISE`, `RESOLVIDA` e `ARQUIVADA`.

---

# 8. Repositories

Repositories ficam em `backend/repositories/`.

A função deles é concentrar consultas que vão além de uma operação simples de Model.

Exemplos importantes:

## EventoRepository

Possui operações como:

- listar eventos ativos;
- vincular evento a trilha;
- listar trilhas de um evento;
- listar eventos de uma trilha;
- listar eventos em que determinado usuário participa;
- verificar participação;
- adicionar/remover participante;
- contar participantes.

A consulta `listar_por_usuario()` faz `JOIN` entre `Evento` e `ParticipanteEvento`, permitindo montar a seção **Minhas expedições**.

## ChecklistRepository

Consulta os equipamentos de determinada trilha e ordena itens obrigatórios antes dos recomendados.

## Repositories de outros recursos

Existem também componentes para favoritos, trilhas, avaliações, histórico e relatórios. Eles evitam colocar consultas especializadas diretamente nos Controllers.

---

# 9. Services

A camada `services` contém regras de negócio e coordena Models e Repositories.

Essa separação é importante porque um Controller não deve decidir regras como quantidade máxima de participantes, cálculo de tempo ou validação de nota.

## Services de casos de uso

Em `services/casos_uso/` existem classes específicas para ações importantes, incluindo:

- cadastrar usuário;
- login;
- atualizar perfil;
- buscar trilhas;
- detalhar trilha;
- listar favoritos;
- adicionar favorito;
- remover favorito;
- listar eventos;
- participar de evento.

O padrão desejado é:

```text
1 caso de uso → 1 Service
```

## TrilhaService

Centraliza funcionalidades relacionadas às trilhas.

Uma regra importante é a estimativa automática de duração. O sistema considera velocidades diferentes conforme a dificuldade, aproximadamente:

```text
Fácil     → 4 km/h
Moderada  → 3 km/h
Difícil   → 2 km/h
```

O tempo estimado é calculado a partir de distância / velocidade.

## EventoService

Coordena a lógica de expedições.

Entre suas responsabilidades estão:

- listar eventos;
- obter eventos de uma trilha;
- obter eventos de um usuário;
- verificar participação;
- criar evento;
- editar/remover quando permitido;
- entrar em evento;
- sair de evento;
- consultar participantes.

Ao criar uma expedição sem coordenadas próprias, o Service pode obter coordenadas de um checkpoint válido da trilha vinculada. Isso permite colocar a expedição no mapa.

O criador é adicionado automaticamente como participante.

## ParticiparEventoService

Executa a regra de entrada em uma expedição.

O fluxo é aproximadamente:

```text
buscar evento
    ↓
verificar se existe
    ↓
verificar se usuário já participa
    ↓
contar vagas ocupadas
    ↓
validar capacidade
    ↓
adicionar participante
```

A operação é idempotente para quem já participa: não cria uma segunda participação.

## FavoritoService

Permite adicionar, remover e listar favoritos. O banco também protege contra duplicação do mesmo favorito.

## AvaliacaoService

Trata avaliações e comentários de trilhas. A nota aceita valores de 1 a 5.

## HistoricoService

Fornece acesso aos registros de trilhas realizadas por determinado usuário.

## ChecklistService

Expõe a leitura do checklist de uma trilha utilizando `ChecklistRepository`.

---

# 10. Controllers REST

Os Controllers REST recebem requisições em `/api`.

Exemplos de recursos:

```text
/api/usuarios/...
/api/trilhas/...
/api/avaliacoes/...
/api/favoritos/...
/api/checkpoints/...
/api/fotos/...
/api/eventos/...
/api/notificacoes/...
/api/denuncias/...
/api/historico/...
/api/relatorios/...
```

O Controller deve fazer principalmente quatro coisas:

```text
receber HTTP
→ interpretar parâmetros/JSON
→ chamar Service
→ transformar resultado em resposta HTTP/JSON
```

Regras de negócio devem permanecer nos Services.

---

# 11. WebController

`backend/controllers/web_controller.py` é o Controller responsável pelo site Jinja2.

Ele instancia os Services necessários e atende páginas como:

```text
/
/home
/mapa
/login
/cadastro
/trilhas/<id>
/favoritos
/eventos
/perfil
```

Também recebe ações POST como:

```text
/logout
/trilhas/<id>/avaliacoes
/trilhas/<id>/favorito
/eventos
/eventos/<id>/participar
/eventos/<id>/sair
```

## Autenticação web

O usuário autenticado é identificado por:

```python
session["id_usuario"]
```

O decorator `login_web_obrigatorio` protege operações que exigem conta. Quando o usuário não está autenticado, ele é enviado à página de login.

## Página inicial

O Controller recebe:

- texto de busca;
- filtro de dificuldade.

Consulta as trilhas e expedições e também identifica favoritos do usuário autenticado.

## Detalhes da trilha

A página reúne informações provenientes de vários componentes:

```text
TrilhaService       → dados da trilha
CheckpointService   → rota GPS
EventoService       → expedições vinculadas
AvaliacaoService    → comentários e notas
ChecklistService    → equipamentos
FavoritoService     → estado de favorito
```

Essa página demonstra bem a função de um Controller como coordenador da interface sem mover toda a regra de negócio para o template.

## Perfil

A página de perfil reúne:

- quantidade de favoritos;
- expedições em que o usuário participa;
- histórico de trilhas realizadas.

Para o histórico, cada entrada pode combinar informações de `HistoricoTrilha`, `Trilha` e `Evento`.

---

# 12. Templates Jinja2

Os arquivos ficam em `backend/templates/`.

## `base.html`

Define a estrutura visual comum, navegação e blocos reutilizados pelas páginas.

## `home.html`

Página inicial com busca, filtros, trilhas e expedições.

## `trail_detail.html`

É uma das páginas mais completas. Exibe:

- informações da trilha;
- distância;
- dificuldade;
- tempo estimado;
- imagem/localização;
- botão de favorito;
- mapa e rota;
- checklist;
- avaliações e comentários;
- expedições relacionadas.

## `events.html`

Exibe as expedições e permite criar/participar/sair. Quando o usuário já está inscrito, a interface identifica a participação.

## `profile.html`

Exibe dados do usuário, favoritos, **Minhas expedições** e o histórico de trilhas/expedições realizadas.

## Outros templates

Há páginas específicas para login, cadastro, favoritos e erros HTTP.

---

# 13. MapLibre GL JS + OpenFreeMap

O sistema não depende mais do Google Maps.

A divisão de responsabilidades é:

```text
OpenFreeMap → fornece o mapa-base
MapLibre GL JS → renderiza e controla o mapa
TrailUp/MySQL → fornece os checkpoints da rota
```

## Rota da trilha

O backend envia os checkpoints ao template. No JavaScript eles são convertidos de:

```text
latitude, longitude
```

para a ordem GeoJSON:

```text
[longitude, latitude]
```

Em seguida é criada uma geometria:

```json
{
  "type": "LineString",
  "coordinates": []
}
```

Ela é adicionada ao MapLibre como uma source GeoJSON e desenhada como uma layer do tipo `line`.

A rota utiliza o verde da identidade visual do TrailUp:

```text
#3DB861
```

O início e o fim recebem marcadores distintos. O mapa calcula os limites dos checkpoints com `LngLatBounds`, enquadra a rota com `fitBounds()` e restringe a navegação a uma área ao redor dela com `setMaxBounds()`.

## Mapa de expedições

A página `/mapa` recebe expedições que possuem latitude e longitude. Cada uma é transformada em um marcador MapLibre. O popup mostra informações básicas da expedição.

## Dependência externa

O mapa-base é carregado do OpenFreeMap e a biblioteca MapLibre é carregada no navegador. Portanto, o recurso necessita de internet, mas não de chave privada de API.

---

# 14. Banco de dados

O schema oficial fica em:

```text
backend/database/create_database.sql
```

Ele cria `trilhas_db` usando `utf8mb4`.

Tabelas atuais incluem:

```text
usuario
trilha
checklist_item
evento
avaliacao
favorito
checkpoint
foto
evento_trilha
participante_evento
notificacao
denuncia
historicoTrilha
registroRealizado
fotoRegistro
```

## Integridade

O banco utiliza:

- Primary Keys;
- Foreign Keys;
- índices;
- `UNIQUE`;
- `CHECK`;
- `CASCADE`;
- `SET NULL`;
- `RESTRICT`.

Exemplos de validação no banco:

- avaliação entre 1 e 5;
- latitude entre -90 e 90;
- longitude entre -180 e 180;
- distância não negativa;
- tempo não negativo;
- vagas positivas;
- estados válidos de denúncia.

## Atenção ao banco existente

Alterar `create_database.sql` no Git não modifica automaticamente uma instalação MySQL já criada.

Por exemplo, quando `checklist_item` foi acrescentada ao projeto, bancos criados antes dessa alteração não receberam a tabela automaticamente. Nesses casos é necessário executar o `CREATE TABLE` correspondente ou recriar o banco a partir do schema atual.

---

# 15. Stored Procedures e relatórios

O arquivo:

```text
backend/database/procedures_relatorios.sql
```

contém procedures de relatório.

Entre as consultas projetadas estão:

### `sp_trilhas_por_dificuldade`

Produz informações de trilhas agrupando também dados como avaliações, favoritos e realizações.

### `sp_resumo_usuario`

Gera um resumo estatístico de determinado usuário, como trilhas concluídas, distância, tempo, favoritos, avaliações e eventos.

### `sp_ranking_usuarios`

Gera ranking considerando atividades dos usuários.

### `sp_favoritos_usuario`

Obtém os favoritos de um usuário com informações das trilhas.

### `sp_eventos_ativos`

Retorna expedições ativas e informações relacionadas.

---

# 16. Funcionalidades principais e fluxo completo

## 16.1 Cadastro

```text
Formulário
→ WebController
→ CadastrarUsuarioService
→ Usuario
→ MySQL
```

Após o cadastro, a sessão web recebe o ID do usuário.

## 16.2 Login

```text
E-mail + senha
→ WebController
→ LoginUsuarioService
→ validação do Usuario
→ session["id_usuario"]
```

## 16.3 Buscar trilhas

```text
Campo de busca/filtro
→ WebController
→ TrilhaService/BuscarTrilhasService
→ Repository
→ MySQL
→ cards na homepage
```

## 16.4 Visualizar trilha

Reúne dados de trilha, checkpoints, avaliações, checklist, eventos e favoritos.

## 16.5 Favoritar

```text
Botão Favoritar
→ WebController
→ FavoritoService
→ Favorito/Repository
→ MySQL
```

## 16.6 Comentários e avaliações

```text
Nota + comentário
→ WebController
→ AvaliacaoService
→ Avaliacao
→ MySQL
```

Depois as avaliações são carregadas junto com o nome do autor e mostradas na página da trilha.

## 16.7 Checklist

```text
Página da trilha
→ WebController
→ ChecklistService
→ ChecklistRepository
→ ChecklistItem
→ MySQL
```

A interface mostra os itens como caixas marcáveis.

## 16.8 Criar expedição

```text
Formulário de evento
→ WebController
→ EventoService
→ Evento + EventoTrilha + ParticipanteEvento
→ MySQL
```

O criador passa a participar automaticamente.

## 16.9 Participar de expedição

```text
Participar
→ WebController
→ EventoService
→ ParticiparEventoService
→ EventoRepository
→ ParticipanteEvento
→ MySQL
```

Antes da inserção são verificadas existência, participação anterior e vagas.

## 16.10 Minhas expedições

```text
Perfil
→ EventoService.listar_por_usuario
→ EventoRepository
→ JOIN participante_evento/evento
→ MySQL
```

A interface informa explicitamente quais expedições pertencem ao usuário.

## 16.11 Histórico

```text
Perfil
→ HistoricoService
→ registros HistoricoTrilha
→ dados de Trilha e Evento
→ histórico na interface
```

---

# 17. Autenticação e segurança

O projeto possui autenticação para API e sessão para o site.

As senhas não devem ser armazenadas em texto puro. O backend utiliza mecanismos do Werkzeug para geração e verificação de hash.

A API possui mecanismo de token assinado e rotas protegidas. O site utiliza a sessão Flask.

Pontos positivos:

- hash de senha;
- `SECRET_KEY` configurável por ambiente;
- validações de autorização em operações como edição de evento;
- Foreign Keys e restrições de integridade;
- rollback em erro de banco.

Pontos que merecem atenção em produção:

- a `SECRET_KEY` padrão deve obrigatoriamente ser substituída;
- CORS está configurado como `*`, adequado para desenvolvimento mas amplo demais para produção;
- `DEBUG` deve ficar desligado em produção;
- credenciais do MySQL devem vir do ambiente;
- formulários web poderiam receber proteção CSRF dedicada;
- dependências JS externas podem ser fixadas/servidas localmente caso seja necessária maior previsibilidade.

---

# 18. SOLID e separação de responsabilidades

## SRP — Single Responsibility Principle

É o princípio mais claramente aplicado. Models, Controllers, Services e Repositories possuem papéis diferentes, e vários casos de uso têm Services próprios.

## OCP — Open/Closed Principle

É parcialmente atendido. A separação em camadas facilita adicionar novas funcionalidades, mas algumas classes ainda dependem diretamente de implementações concretas.

## LSP — Liskov Substitution Principle

Há pouco uso de hierarquias/interfaces polimórficas no projeto, então o princípio aparece pouco na prática.

## ISP — Interface Segregation Principle

Não existem interfaces formais para a maioria dos Repositories/Services. Assim, o projeto não explora fortemente esse princípio.

## DIP — Dependency Inversion Principle

É um ponto de melhoria. Alguns Services criam diretamente seus Repositories concretos, por exemplo conceitualmente:

```python
self.repository = EventoRepository()
```

Uma arquitetura com injeção de dependência permitiria:

```python
class Service:
    def __init__(self, repository):
        self.repository = repository
```

Isso facilitaria testes unitários com repositories falsos/mocks e reduziria acoplamento.

### Conclusão sobre SOLID

O projeto possui **boa separação em camadas**, especialmente quanto a SRP, mas não deve ser descrito como aplicação completa de todos os princípios SOLID.

---

# 19. Pontos fortes

O código apresenta várias decisões positivas:

1. frontend e API reutilizam a mesma lógica de backend;
2. regras importantes são retiradas dos templates;
3. existe separação Controller/Service/Model/Repository;
4. SQLAlchemy centraliza o mapeamento objeto-relacional;
5. MySQL possui restrições de integridade adicionais;
6. favoritos são idempotentes/protegidos contra duplicação;
7. participação em expedições verifica capacidade;
8. checkpoints são reutilizados para construir rotas reais;
9. MapLibre elimina a necessidade de chave do Google Maps;
10. histórico, checklist e participação em expedições estão integrados à interface;
11. existem Stored Procedures para relatórios;
12. existe API REST além do frontend web.

---

# 20. Pontos de melhoria encontrados

## 20.1 Controllers REST inconsistentes

A arquitetura da atividade pede Controllers como classes. Parte dos Controllers REST existentes ainda utiliza uma estrutura funcional. Isso deve ser uniformizado caso a avaliação exija literalmente Controllers orientados a classes.

## 20.2 Services muito amplos

Alguns Services funcionam como facades com várias operações. Para seguir estritamente a regra de “um caso de uso por Service”, novas ações podem ser extraídas para classes específicas.

## 20.3 Dependency Injection

Os Services ainda conhecem implementações concretas de Repository. Injeção de dependência melhoraria testabilidade e DIP.

## 20.4 CRUD duplicado em Repository

Operações CRUD simples podem permanecer nos Models quando essa é a convenção da atividade. Repository deve ser preferido para consultas especiais, filtros, rankings e relatórios.

## 20.5 Documentação desatualizada

Alguns comentários e READMEs antigos ainda podem mencionar Google Maps, apesar de o código ativo já utilizar MapLibre + OpenFreeMap. A documentação deve ser sincronizada antes da entrega final.

## 20.6 Testes antigos

Há testes associados à fase anterior de migração web/Google Maps que precisam ser revisados para refletir a arquitetura atual.

## 20.7 Banco sem sistema automático de migrations

O projeto usa scripts SQL como fonte de criação do banco. Isso é simples para a atividade, porém significa que alterações de schema não são aplicadas automaticamente em bancos já existentes. Foi exatamente o motivo do erro `Table 'trilhas_db.checklist_item' doesn't exist` em uma instalação criada antes da tabela.

Uma aplicação de produção poderia usar Alembic/Flask-Migrate, mas isso não é obrigatório para o funcionamento atual.

## 20.8 Checklist no navegador

Os itens do checklist são persistidos como definição de equipamento por trilha, mas o estado visual de cada checkbox marcado pelo usuário não representa atualmente uma persistência individual de “item concluído por usuário”. Se for necessário guardar o progresso do checklist, seria necessária uma entidade associativa adicional.

---

# 21. Fluxo completo do sistema

Exemplo de uma utilização típica:

```text
Usuário abre TrailUp
        ↓
cria conta / faz login
        ↓
pesquisa uma trilha
        ↓
abre detalhes
        ↓
visualiza informações
        ↓
visualiza rota MapLibre
        ↓
consulta equipamentos
        ↓
favorita a trilha
        ↓
consulta expedições
        ↓
participa de uma expedição
        ↓
participante_evento é atualizado
        ↓
perfil mostra “Minhas expedições”
        ↓
após realização, historicoTrilha registra atividade
        ↓
perfil mostra o histórico
        ↓
usuário pode avaliar/comentar a trilha
```

---

# 22. Fluxo do mapa em detalhes

```text
Tabela checkpoint
       ↓
Checkpoint Model
       ↓
CheckpointService
       ↓
WebController.trilha()
       ↓
checkpoints enviados ao Jinja2
       ↓
JavaScript converte para [longitude, latitude]
       ↓
GeoJSON LineString
       ↓
MapLibre addSource()
       ↓
MapLibre addLayer(type="line")
       ↓
rota desenhada sobre OpenFreeMap
```

O mapa-base e a rota são conceitos separados. OpenFreeMap fornece ruas, áreas e elementos cartográficos; a rota específica do TrailUp vem exclusivamente do banco.

---

# 23. Fluxo de expedições em detalhes

A relação é:

```text
Usuario
   │
   ├── cria → Evento
   │
   └── participa
          ↓
ParticipanteEvento
          ↓
        Evento
          ↓
     EventoTrilha
          ↓
        Trilha
```

Assim, ser criador e ser participante são conceitos relacionados, mas diferentes. O criador é automaticamente inserido como participante no momento da criação.

---

# 24. Fluxo do histórico

```text
Usuario
   ↓
HistoricoTrilha
   ├── Trilha
   ├── Evento (opcional)
   └── RegistroRealizado
          ↓
       FotoRegistro
```

Essa estrutura permite guardar tanto um resumo da realização quanto registros GPS e fotos associados.

---

# 25. Como executar

## Criar o banco

Dentro de `backend`:

```bash
mysql -u root -P 3307 -p < database/create_database.sql
mysql -u root -P 3307 -p < database/procedures_relatorios.sql
```

A porta deve ser ajustada caso a instalação local utilize outra porta, como 3306.

## Ambiente Python

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
pip install -r requirements.txt
$env:DATABASE_URL="mysql+pymysql://root:SUA_SENHA@localhost:3307/trilhas_db"
$env:SECRET_KEY="uma-chave-segura"
py app.py
```

Não é necessária chave para o MapLibre/OpenFreeMap.

Depois:

```text
http://localhost:5000/
```

---

# 26. Resumo para apresentação

Uma explicação curta e tecnicamente correta do projeto seria:

> O TrailUp é uma aplicação web Flask organizada em camadas. O frontend é renderizado com Jinja2 e reutiliza os mesmos Services utilizados pela API REST. Os Controllers recebem as requisições, os Services concentram regras de negócio, os Models SQLAlchemy representam as tabelas e os Repositories executam consultas especializadas. Os dados são armazenados em MySQL. As trilhas possuem checkpoints GPS que são enviados ao frontend e transformados em uma LineString GeoJSON, desenhada pelo MapLibre GL JS sobre o mapa-base do OpenFreeMap. O sistema também possui favoritos, avaliações, checklist de equipamentos, expedições com controle de participantes, histórico de trilhas, notificações, denúncias e relatórios.

---

# 27. Conclusão

O TrailUp evoluiu de um frontend Flutter para uma aplicação web Flask/Jinja2 mantendo um backend REST e banco MySQL. A arquitetura atual possui uma separação clara entre interface, Controllers, Services, Models/Repositories e banco.

As funcionalidades mais importantes já possuem integração de ponta a ponta, incluindo autenticação, busca e detalhes de trilhas, favoritos, avaliações, expedições, participação, checklist, histórico e visualização cartográfica.

A troca para **MapLibre GL JS + OpenFreeMap** reduziu dependência de serviços pagos e eliminou a necessidade de uma chave Google para o mapa. Os checkpoints continuam pertencendo ao próprio domínio TrailUp e formam a rota da trilha.

Para uma entrega acadêmica mais rigorosa, os principais próximos ajustes são uniformizar todos os Controllers REST como classes, separar Services restantes por caso de uso quando necessário, revisar testes/documentação antiga e aumentar a cobertura automatizada. Para uma evolução de produção, também seriam recomendáveis migrations de banco, CSRF, CORS restrito, injeção de dependência e configurações de segurança específicas de produção.
