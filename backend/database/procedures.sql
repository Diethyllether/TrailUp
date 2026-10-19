USE trilhas_db;

DROP PROCEDURE IF EXISTS sp_resumo_usuario;
DROP PROCEDURE IF EXISTS sp_ranking_usuarios;
DROP PROCEDURE IF EXISTS sp_favoritos_usuario;
DROP PROCEDURE IF EXISTS sp_eventos_ativos;
DROP PROCEDURE IF EXISTS sp_checklist_usuario;
DROP PROCEDURE IF EXISTS sp_trilhas_proximas;
DROP PROCEDURE IF EXISTS sp_buscar_trilhas;
DROP PROCEDURE IF EXISTS sp_filtrar_trilhas;
DROP PROCEDURE IF EXISTS sp_medias_trilhas;
DROP PROCEDURE IF EXISTS sp_avaliacoes_trilha;
DROP PROCEDURE IF EXISTS sp_historico_usuario;
DROP PROCEDURE IF EXISTS sp_checkpoints_validos;
DROP PROCEDURE IF EXISTS sp_checkpoints_trilha;
DROP PROCEDURE IF EXISTS sp_primeiro_checkpoint_valido;
DROP PROCEDURE IF EXISTS sp_trilhas_evento;
DROP PROCEDURE IF EXISTS sp_eventos_por_trilha;
DROP PROCEDURE IF EXISTS sp_eventos_por_usuario;
DROP PROCEDURE IF EXISTS sp_participantes_evento;
DROP PROCEDURE IF EXISTS sp_comentarios_evento;
DROP PROCEDURE IF EXISTS sp_contar_participantes_evento;
DROP PROCEDURE IF EXISTS sp_detalhes_eventos;

DELIMITER $$

CREATE PROCEDURE sp_buscar_trilhas(
    IN p_termo VARCHAR(200),
    IN p_dificuldade VARCHAR(50)
)
BEGIN
    SELECT t.idTrilha, t.nome, t.localizacao, t.distancia, t.duracao,
           t.dificuldade, t.descricao, t.imagemUrl, t.tempoEstimadoMin
      FROM trilha t
     WHERE (p_termo IS NULL OR p_termo = ''
            OR t.nome LIKE CONCAT('%', p_termo, '%')
            OR t.localizacao LIKE CONCAT('%', p_termo, '%'))
       AND (p_dificuldade IS NULL OR p_dificuldade = ''
            OR t.dificuldade = p_dificuldade)
     ORDER BY t.nome ASC;
END$$

CREATE PROCEDURE sp_filtrar_trilhas(
    IN p_distancia_max FLOAT,
    IN p_duracao_max FLOAT,
    IN p_nota_min FLOAT,
    IN p_ordem VARCHAR(20)
)
BEGIN
    SELECT t.idTrilha, t.nome, t.localizacao, t.distancia, t.duracao,
           t.dificuldade, t.descricao, t.imagemUrl, t.tempoEstimadoMin,
           av.media, av.quantidade
      FROM trilha t
      LEFT JOIN (
          SELECT idTrilha, AVG(nota) AS media, COUNT(*) AS quantidade
            FROM avaliacao GROUP BY idTrilha
      ) av ON av.idTrilha = t.idTrilha
     WHERE (p_distancia_max IS NULL OR t.distancia <= p_distancia_max)
       AND (p_duracao_max IS NULL OR t.duracao <= p_duracao_max)
       AND (p_nota_min IS NULL OR COALESCE(av.media, 0) >= p_nota_min)
     ORDER BY
       CASE WHEN p_ordem = 'distancia' THEN t.distancia END ASC,
       CASE WHEN p_ordem = 'duracao' THEN t.duracao END ASC,
       CASE WHEN p_ordem = 'nota' THEN av.media END DESC,
       t.nome ASC;
END$$

CREATE PROCEDURE sp_medias_trilhas()
BEGIN
    SELECT t.idTrilha, AVG(a.nota) AS media, COUNT(a.idAvaliacao) AS quantidade
      FROM trilha t
      LEFT JOIN avaliacao a ON a.idTrilha = t.idTrilha
     GROUP BY t.idTrilha;
END$$

CREATE PROCEDURE sp_avaliacoes_trilha(IN p_id_trilha INT)
BEGIN
    SELECT a.idAvaliacao, a.nota, a.comentario, a.data, a.idUsuario,
           a.idTrilha, u.nome AS nomeUsuario
      FROM avaliacao a
      JOIN usuario u ON u.idUsuario = a.idUsuario
     WHERE a.idTrilha = p_id_trilha
     ORDER BY a.data DESC, a.idAvaliacao DESC;
END$$

CREATE PROCEDURE sp_historico_usuario(IN p_id_usuario INT)
BEGIN
    SELECT h.idHistorico, h.dataRealizacao, h.tempo, h.avaliacaoPessoal,
           h.idUsuario, h.idEvento, h.idTrilha, t.nome AS nomeTrilha
      FROM historicoTrilha h
      JOIN trilha t ON t.idTrilha = h.idTrilha
     WHERE h.idUsuario = p_id_usuario
     ORDER BY h.dataRealizacao DESC, h.idHistorico DESC;
END$$

CREATE PROCEDURE sp_checkpoints_validos()
BEGIN
    SELECT idCheckpoint, latitude, longitude, horario, idTrilha
      FROM checkpoint
     WHERE latitude BETWEEN -90 AND 90 AND longitude BETWEEN -180 AND 180
       AND NOT (latitude = 0 AND longitude = 0)
     ORDER BY idCheckpoint;
END$$

CREATE PROCEDURE sp_checkpoints_trilha(IN p_id_trilha INT)
BEGIN
    SELECT idCheckpoint, latitude, longitude, horario, idTrilha
      FROM checkpoint
     WHERE idTrilha = p_id_trilha
     ORDER BY idCheckpoint;
END$$

CREATE PROCEDURE sp_primeiro_checkpoint_valido(IN p_id_trilha INT)
BEGIN
    SELECT idCheckpoint, latitude, longitude, horario, idTrilha
      FROM checkpoint
     WHERE idTrilha = p_id_trilha
       AND latitude BETWEEN -90 AND 90 AND longitude BETWEEN -180 AND 180
       AND NOT (latitude = 0 AND longitude = 0)
     ORDER BY idCheckpoint
     LIMIT 1;
END$$

CREATE PROCEDURE sp_trilhas_evento(IN p_id_evento INT)
BEGIN
    SELECT idEvento, idTrilha FROM evento_trilha WHERE idEvento = p_id_evento;
END$$

CREATE PROCEDURE sp_eventos_por_trilha(IN p_id_trilha INT)
BEGIN
    SELECT e.idEvento, e.titulo, e.descricao, e.data, e.horarioSaida,
           e.imediata, e.vagas, e.tipo, e.latitude, e.longitude, e.idCriador
      FROM evento e
      JOIN evento_trilha et ON et.idEvento = e.idEvento
     WHERE et.idTrilha = p_id_trilha
     ORDER BY e.data, e.horarioSaida, e.idEvento;
END$$

CREATE PROCEDURE sp_eventos_por_usuario(IN p_id_usuario INT)
BEGIN
    SELECT e.idEvento, e.titulo, e.descricao, e.data, e.horarioSaida,
           e.imediata, e.vagas, e.tipo, e.latitude, e.longitude, e.idCriador
      FROM evento e
      JOIN participante_evento pe ON pe.idEvento = e.idEvento
     WHERE pe.idUsuario = p_id_usuario
     ORDER BY e.data DESC, e.horarioSaida DESC, e.idEvento DESC;
END$$

CREATE PROCEDURE sp_participantes_evento(IN p_id_evento INT)
BEGIN
    SELECT pe.idUsuario, pe.idEvento, u.nome
      FROM participante_evento pe
      JOIN usuario u ON u.idUsuario = pe.idUsuario
     WHERE pe.idEvento = p_id_evento
     ORDER BY u.nome;
END$$

CREATE PROCEDURE sp_comentarios_evento(IN p_id_evento INT)
BEGIN
    SELECT c.idComentario, c.texto, c.dataEnvio, c.idUsuario, c.idEvento,
           u.nome AS nomeUsuario
      FROM comentario_evento c
      JOIN usuario u ON u.idUsuario = c.idUsuario
     WHERE c.idEvento = p_id_evento
     ORDER BY c.dataEnvio ASC, c.idComentario ASC;
END$$

CREATE PROCEDURE sp_contar_participantes_evento(IN p_id_evento INT)
BEGIN
    SELECT COUNT(*) AS quantidade
      FROM participante_evento WHERE idEvento = p_id_evento;
END$$

CREATE PROCEDURE sp_detalhes_eventos(IN p_ids JSON)
BEGIN
    SELECT e.idEvento,
           (SELECT JSON_ARRAYAGG(et.idTrilha)
              FROM evento_trilha et WHERE et.idEvento = e.idEvento) AS trilhasIds,
           (SELECT JSON_ARRAYAGG(u.nome)
              FROM participante_evento pe
              JOIN usuario u ON u.idUsuario = pe.idUsuario
             WHERE pe.idEvento = e.idEvento) AS participantes,
           (SELECT COUNT(*) FROM participante_evento pe
             WHERE pe.idEvento = e.idEvento) AS participantesAtuais,
           (SELECT JSON_ARRAYAGG(JSON_OBJECT(
                       'idComentario', c.idComentario, 'texto', c.texto,
                       'dataEnvio', c.dataEnvio, 'nomeUsuario', u.nome))
              FROM comentario_evento c
              JOIN usuario u ON u.idUsuario = c.idUsuario
             WHERE c.idEvento = e.idEvento) AS comentarios,
           criador.nome AS nomeCriador
      FROM JSON_TABLE(p_ids, '$[*]' COLUMNS(idEvento INT PATH '$')) ids
      JOIN evento e ON e.idEvento = ids.idEvento
      JOIN usuario criador ON criador.idUsuario = e.idCriador;
END$$

-- ============================================================
-- Lista trilhas de uma dificuldade específica ou todas quando
-- p_dificuldade for NULL. Inclui métricas úteis para os cards web.
-- ============================================================
-- ============================================================
-- Retorna um resumo completo do perfil do usuário para dashboards.
-- Mantém as colunas já usadas pelo projeto e acrescenta distância,
-- tempo total e participação em eventos.
-- ============================================================
CREATE PROCEDURE sp_resumo_usuario(
    IN p_id_usuario INT
)
BEGIN
    SELECT
        u.idUsuario,
        u.nome,
        u.email,
        u.fotoPerfil,
        u.dataCadastro,
        COALESCE(hist.trilhasRealizadas, 0) AS trilhasRealizadas,
        COALESCE(hist.distanciaTotalKm, 0) AS distanciaTotalKm,
        COALESCE(hist.tempoTotalMin, 0) AS tempoTotalMin,
        COALESCE(fav.totalFavoritos, 0) AS totalFavoritos,
        COALESCE(av.totalAvaliacoes, 0) AS totalAvaliacoes,
        COALESCE(av.mediaNotasDadas, 0) AS mediaNotasDadas,
        COALESCE(evt.eventosParticipados, 0) AS eventosParticipados
    FROM usuario u
    LEFT JOIN (
        SELECT
            h.idUsuario,
            COUNT(*) AS trilhasRealizadas,
            ROUND(COALESCE(SUM(t.distancia), 0), 2) AS distanciaTotalKm,
            ROUND(COALESCE(SUM(h.tempo), 0), 2) AS tempoTotalMin
        FROM historicoTrilha h
        JOIN trilha t ON t.idTrilha = h.idTrilha
        GROUP BY h.idUsuario
    ) hist ON hist.idUsuario = u.idUsuario
    LEFT JOIN (
        SELECT
            idUsuario,
            COUNT(*) AS totalFavoritos
        FROM favorito
        GROUP BY idUsuario
    ) fav ON fav.idUsuario = u.idUsuario
    LEFT JOIN (
        SELECT
            idUsuario,
            COUNT(*) AS totalAvaliacoes,
            ROUND(AVG(nota), 2) AS mediaNotasDadas
        FROM avaliacao
        GROUP BY idUsuario
    ) av ON av.idUsuario = u.idUsuario
    LEFT JOIN (
        SELECT
            idUsuario,
            COUNT(*) AS eventosParticipados
        FROM participante_evento
        GROUP BY idUsuario
    ) evt ON evt.idUsuario = u.idUsuario
    WHERE u.idUsuario = p_id_usuario;
END$$

-- ============================================================
-- Ranking da comunidade. O critério principal é quantidade de trilhas
-- concluídas; distância total e avaliações funcionam como desempate.
-- ============================================================
CREATE PROCEDURE sp_ranking_usuarios(
    IN p_limite INT
)
BEGIN
    DECLARE v_limite INT DEFAULT 10;

    IF p_limite IS NOT NULL AND p_limite BETWEEN 1 AND 100 THEN
        SET v_limite = p_limite;
    END IF;

    SELECT
        u.idUsuario,
        u.nome,
        u.fotoPerfil,
        COALESCE(hist.trilhasConcluidas, 0) AS trilhasConcluidas,
        COALESCE(hist.distanciaTotalKm, 0) AS distanciaTotalKm,
        COALESCE(av.avaliacoesRealizadas, 0) AS avaliacoesRealizadas
    FROM usuario u
    LEFT JOIN (
        SELECT
            h.idUsuario,
            COUNT(*) AS trilhasConcluidas,
            ROUND(COALESCE(SUM(t.distancia), 0), 2) AS distanciaTotalKm
        FROM historicoTrilha h
        JOIN trilha t ON t.idTrilha = h.idTrilha
        GROUP BY h.idUsuario
    ) hist ON hist.idUsuario = u.idUsuario
    LEFT JOIN (
        SELECT
            idUsuario,
            COUNT(*) AS avaliacoesRealizadas
        FROM avaliacao
        GROUP BY idUsuario
    ) av ON av.idUsuario = u.idUsuario
    ORDER BY
        trilhasConcluidas DESC,
        distanciaTotalKm DESC,
        avaliacoesRealizadas DESC,
        u.nome ASC
    LIMIT v_limite;
END$$

-- ============================================================
-- Favoritos detalhados do usuário com dados prontos para os cards.
-- ============================================================
CREATE PROCEDURE sp_favoritos_usuario(
    IN p_id_usuario INT
)
BEGIN
    SELECT
        f.idFavorito,
        f.dataSalvo,
        t.idTrilha,
        t.nome,
        t.localizacao,
        t.distancia,
        t.dificuldade,
        t.tempoEstimadoMin,
        t.imagemUrl,
        COALESCE(av.mediaNota, 0) AS mediaNota,
        COALESCE(av.quantidadeAvaliacoes, 0) AS quantidadeAvaliacoes
    FROM favorito f
    JOIN trilha t
        ON t.idTrilha = f.idTrilha
    LEFT JOIN (
        SELECT
            idTrilha,
            ROUND(AVG(nota), 2) AS mediaNota,
            COUNT(*) AS quantidadeAvaliacoes
        FROM avaliacao
        GROUP BY idTrilha
    ) av ON av.idTrilha = t.idTrilha
    WHERE f.idUsuario = p_id_usuario
    ORDER BY
        f.dataSalvo DESC,
        t.nome ASC;
END$$

-- ============================================================
-- Lista expedições atuais/futuras para a página de eventos e mapa.
-- ============================================================
CREATE PROCEDURE sp_eventos_ativos()
BEGIN
    SELECT
        e.idEvento,
        e.titulo,
        e.descricao,
        e.data,
        e.horarioSaida,
        e.imediata,
        e.vagas,
        e.tipo,
        e.latitude,
        e.longitude,
        e.idCriador,
        u.nome AS nomeCriador,
        COALESCE(part.participantesAtuais, 0) AS participantesAtuais,
        trilhas.trilhas
    FROM evento e
    JOIN usuario u
        ON u.idUsuario = e.idCriador
    LEFT JOIN (
        SELECT
            idEvento,
            COUNT(*) AS participantesAtuais
        FROM participante_evento
        GROUP BY idEvento
    ) part ON part.idEvento = e.idEvento
    LEFT JOIN (
        SELECT
            et.idEvento,
            GROUP_CONCAT(t.nome ORDER BY t.nome SEPARATOR ', ') AS trilhas
        FROM evento_trilha et
        JOIN trilha t ON t.idTrilha = et.idTrilha
        GROUP BY et.idEvento
    ) trilhas ON trilhas.idEvento = e.idEvento
    WHERE e.imediata = TRUE
       OR e.data IS NULL
       OR e.data >= CURRENT_DATE
    ORDER BY
        e.imediata DESC,
        e.data ASC,
        e.horarioSaida ASC,
        e.titulo ASC;
END$$

CREATE PROCEDURE sp_checklist_usuario(
    IN p_id_usuario INT,
    IN p_id_trilha INT
)
BEGIN
    SELECT cu.idChecklistItem, cu.marcado
      FROM checklist_usuario cu
      JOIN checklist_item ci ON ci.idChecklistItem = cu.idChecklistItem
     WHERE cu.idUsuario = p_id_usuario
       AND ci.idTrilha = p_id_trilha
     ORDER BY ci.obrigatorio DESC, ci.idChecklistItem ASC;
END$$

CREATE PROCEDURE sp_trilhas_proximas(
    IN p_latitude DOUBLE,
    IN p_longitude DOUBLE,
    IN p_limite INT
)
BEGIN
    SELECT cp.idTrilha,
           MIN(6371 * ACOS(LEAST(1, GREATEST(-1,
               COS(RADIANS(p_latitude)) * COS(RADIANS(cp.latitude)) *
               COS(RADIANS(cp.longitude) - RADIANS(p_longitude)) +
               SIN(RADIANS(p_latitude)) * SIN(RADIANS(cp.latitude))
           )))) AS distanciaKm
      FROM checkpoint cp
     WHERE cp.latitude BETWEEN -90 AND 90
       AND cp.longitude BETWEEN -180 AND 180
       AND NOT (cp.latitude = 0 AND cp.longitude = 0)
     GROUP BY cp.idTrilha
     ORDER BY distanciaKm ASC, cp.idTrilha ASC
     LIMIT p_limite;
END$$

DELIMITER ;
