-- Dados de exemplo do TrailUp (MySQL 8+).
-- Execute depois de create_database.sql e, se aplicavel, migration_recursos_comunidade.sql.
-- Script idempotente: trilhas existentes com estes nomes nao sao duplicadas.
-- A trilha real e a Pedra Bonita, no Parque Nacional da Tijuca (RJ).
-- Coordenada do inicio: -22.985748, -43.279124 (Rio & Learn).
-- Foto original: Lettydornelas, Wikimedia Commons, CC BY-SA 3.0.
-- Credito/licenca e fontes das imagens estao nas legendas e URLs abaixo.

USE trilhas_db;
START TRANSACTION;

INSERT INTO trilha
    (nome, localizacao, distancia, duracao, dificuldade, descricao, imagemUrl, tempoEstimadoMin)
SELECT
    'Pedra Bonita - Parque Nacional da Tijuca',
    'Sao Conrado, Rio de Janeiro - RJ',
    2.6, 90, 'FACIL',
    'Trilha real de ida e volta ate o cume da Pedra Bonita, com vista para a Zona Sul, Sao Conrado e Pedra da Gavea. Distancia aproximada; confirme acesso e condicoes no parque antes da visita.',
    'https://commons.wikimedia.org/wiki/Special:FilePath/Pedra_Bonita-RJ.jpg',
    90
WHERE NOT EXISTS (
    SELECT 1 FROM trilha WHERE nome = 'Pedra Bonita - Parque Nacional da Tijuca'
);

SET @pedra_bonita_id := (SELECT idTrilha FROM trilha WHERE nome = 'Pedra Bonita - Parque Nacional da Tijuca' LIMIT 1);

-- Pontos de referencia aproximados do percurso, iniciando na coordenada publicada.
INSERT INTO checkpoint (latitude, longitude, idTrilha)
SELECT -22.985748, -43.279124, @pedra_bonita_id
WHERE NOT EXISTS (SELECT 1 FROM checkpoint WHERE idTrilha = @pedra_bonita_id);
INSERT INTO checkpoint (latitude, longitude, idTrilha)
SELECT -22.986100, -43.278850, @pedra_bonita_id
WHERE (SELECT COUNT(*) FROM checkpoint WHERE idTrilha = @pedra_bonita_id) = 1;
INSERT INTO checkpoint (latitude, longitude, idTrilha)
SELECT -22.986600, -43.278700, @pedra_bonita_id
WHERE (SELECT COUNT(*) FROM checkpoint WHERE idTrilha = @pedra_bonita_id) = 2;
INSERT INTO checkpoint (latitude, longitude, idTrilha)
SELECT -22.987100, -43.278500, @pedra_bonita_id
WHERE (SELECT COUNT(*) FROM checkpoint WHERE idTrilha = @pedra_bonita_id) = 3;

INSERT INTO foto (url, legenda, idTrilha)
SELECT 'https://commons.wikimedia.org/wiki/Special:FilePath/Pedra_Bonita-RJ.jpg',
       'Vista do topo ao fim da trilha — Lettydornelas, CC BY-SA 3.0; https://commons.wikimedia.org/wiki/File:Pedra_Bonita-RJ.jpg',
       @pedra_bonita_id
WHERE NOT EXISTS (SELECT 1 FROM foto WHERE idTrilha = @pedra_bonita_id AND url LIKE '%Pedra_Bonita-RJ.jpg%');

INSERT INTO checklist_item (descricao, obrigatorio, idTrilha)
SELECT 'Levar agua suficiente e lanche leve', TRUE, @pedra_bonita_id
WHERE NOT EXISTS (SELECT 1 FROM checklist_item WHERE idTrilha = @pedra_bonita_id AND descricao = 'Levar agua suficiente e lanche leve');
INSERT INTO checklist_item (descricao, obrigatorio, idTrilha)
SELECT 'Usar calcado fechado com boa aderencia', TRUE, @pedra_bonita_id
WHERE NOT EXISTS (SELECT 1 FROM checklist_item WHERE idTrilha = @pedra_bonita_id AND descricao = 'Usar calcado fechado com boa aderencia');
INSERT INTO checklist_item (descricao, obrigatorio, idTrilha)
SELECT 'Protetor solar e repelente', FALSE, @pedra_bonita_id
WHERE NOT EXISTS (SELECT 1 FROM checklist_item WHERE idTrilha = @pedra_bonita_id AND descricao = 'Protetor solar e repelente');

-- Trilhas ficticias adicionais para exercitar listagem, filtros e detalhes.
INSERT INTO trilha (nome, localizacao, distancia, duracao, dificuldade, descricao, imagemUrl, tempoEstimadoMin)
SELECT 'Cachoeira do Sossego (demo)', 'Chapada dos Veadeiros, GO', 7.0, 240, 'MODERADA',
       'Registro ficticio para demonstracao da aplicacao; nao usar como navegacao.',
       'https://images.unsplash.com/photo-1432407692634-6434c2260c24?w=800', 240
WHERE NOT EXISTS (SELECT 1 FROM trilha WHERE nome = 'Cachoeira do Sossego (demo)');

SET @cachoeira_id := (SELECT idTrilha FROM trilha WHERE nome = 'Cachoeira do Sossego (demo)' LIMIT 1);
INSERT INTO checkpoint (latitude, longitude, idTrilha)
SELECT -14.1660, -47.7900, @cachoeira_id
WHERE NOT EXISTS (SELECT 1 FROM checkpoint WHERE idTrilha = @cachoeira_id);
INSERT INTO checkpoint (latitude, longitude, idTrilha)
SELECT -14.1690, -47.7860, @cachoeira_id
WHERE (SELECT COUNT(*) FROM checkpoint WHERE idTrilha = @cachoeira_id) = 1;

COMMIT;
