# Apresentação — TrailUp

## 1. Problema e público
Pessoas que praticam trilhas precisam comparar percursos, se preparar e coordenar saídas. O TrailUp reúne busca de trilhas, informações de percurso, avaliações, favoritos e expedições. O público é a comunidade trilheira.

## 2. Casos de uso para demonstrar
- Buscar, filtrar e ordenar trilhas na tela inicial.
- Abrir o detalhe de uma trilha e consultar checkpoints no mapa.
- Participar de uma expedição e conferir participantes.
- Consultar ranking e resumo pessoal.

As duas últimas telas usam relatórios em procedures; teste com MySQL antes da apresentação. A proximidade usa a procedure `sp_trilhas_proximas` via Repository.

## 3. Arquitetura
O frontend estático roda na porta 8000 e chama a API Flask na porta 5000. A API usa Services, Models Active Record e repositories para consultas especializadas. O código ainda possui um módulo único de rotas e Services Facade; a migração para classes Controller e um Service por caso de uso está incompleta.

Consulte [diagrama de classes](diagrama_de_classes.md) e os [fluxogramas](fluxogramas/).

## 4. Tecnologias
Python, Flask, SQLAlchemy, MySQL, HTML, CSS, JavaScript e MapLibre GL.

## 5. Execução
Siga os passos de configuração de banco, `.env` e inicialização dos dois servidores em [README](../README.md#instalação-e-execução).
