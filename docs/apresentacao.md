# Apresentação — TrailUp

## Projeto e público

O TrailUp organiza a descoberta e preparação de trilhas e a coordenação de expedições. É voltado a pessoas que fazem trilhas, de forma individual ou em grupo.

## Arquitetura

O frontend estático é servido em `http://localhost:8000` e consome a API Flask em `http://localhost:5000` por `fetch`. A API organiza rotas em Blueprints, Controllers por recurso, Services por caso de uso, Models para operações CRUD e Repositories para consultas em procedures MySQL.

```text
Tela → fetch → Blueprint → Controller → Service → Model ou Repository → procedure → MySQL
```

Consulte o [diagrama de classes](diagrama_de_classes.md) e os [fluxogramas](fluxogramas/).

## Funcionalidades para apresentar

- Buscar, filtrar e ordenar trilhas.
- Encontrar trilhas próximas das coordenadas informadas.
- Participar de expedição com verificação de vagas.
- Consultar ranking e resumo pessoal.

Ranking, resumo, busca e participação usam procedures MySQL. Faça a demonstração com schema, procedures e seed carregados. O roteiro tem duração máxima de dois minutos em [roteiro_video.md](roteiro_video.md).

## Tecnologias

Python, Flask, Flask-SQLAlchemy, MySQL, HTML, CSS, JavaScript, MapLibre GL e OpenStreetMap.

## Execução

Siga as instruções de banco e dos servidores separados no [README](../README.md#como-executar).
