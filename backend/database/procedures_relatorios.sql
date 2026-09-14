USE trilhas_db;

DROP PROCEDURE IF EXISTS sp_trilhas_por_dificuldade;
DROP PROCEDURE IF EXISTS sp_resumo_usuario;
DROP PROCEDURE IF EXISTS sp_ranking_usuarios;
DROP PROCEDURE IF EXISTS sp_favoritos_usuario;
DROP PROCEDURE IF EXISTS sp_eventos_ativos;

DELIMITER $$

-- ============================================================
-- Lista trilhas de uma dificuldade específica ou todas quando
-- p_dificuldade for NULL. Inclui métricas úteis para os cards web.
-- ============================================================
CREATE PROCEDURE sp_trilhas_por_dificuldade(
    IN p_dificuldade VARCHAR(50)
)
BEGIN
    SELECT
        t.idTrilha,
        t.nome,
        t.localizacao,
        t.distancia,
        t.duracao,
        t.dificuldade,
        t.tempoEstimadoMin,
        t.imagemUrl,
        ROUND(COALESCE(AVG(a.nota), 0), 2) AS mediaNota,
        COUNT(DISTINCT a.idAvaliacao) AS quantidadeAvaliacoes,
        COUNT(DISTINCT f.idFavorito) AS quantidadeFavoritos,
        COUNT(DISTINCT h.idHistorico) AS quantidadeConclusoes
    FROM trilha t
    LEFT JOIN avaliacao a
        ON a.idTrilha = t.idTrilha
    LEFT JOIN favorito f
        ON f.idTrilha = t.idTrilha
    LEFT JOIN historicoTrilha h
        ON h.idTrilha = t.idTrilha
    WHERE p_dificuldade IS NULL
       OR p_dificuldade = ''
       OR t.dificuldade = p_dificuldade
    GROUP BY
        t.idTrilha,
        t.nome,
        t.localizacao,
        t.distancia,
        t.duracao,
        t.dificuldade,
        t.tempoEstimadoMin,
        t.imagemUrl
    ORDER BY
        mediaNota DESC,
        quantidadeAvaliacoes DESC,
        quantidadeFavoritos DESC,
        t.nome ASC;
END$$

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
        COUNT(DISTINCT h.idHistorico) AS trilhasRealizadas,
        ROUND(COALESCE(SUM(DISTINCT_CASE.valor_distancia), 0), 2) AS distanciaTotalKm,
        ROUND(COALESCE(SUM(DISTINCT_CASE.valor_tempo), 0), 2) AS tempoTotalMin,
        COUNT(DISTINCT f.idFavorito) AS totalFavoritos,
        COUNT(DISTINCT av.idAvaliacao) AS totalAvaliacoes,
        ROUND(COALESCE(AVG(av.nota), 0), 2) AS mediaNotasDadas,
        COUNT(DISTINCT pe.idEvento) AS eventosParticipados
    FROM usuario u
    LEFT JOIN historicoTrilha h
        ON h.idUsuario = u.idUsuario
    LEFT JOIN (
        SELECT
            h2.idHistorico,
            COALESCE(t2.distancia, 0) AS valor_distancia,
            COALESCE(h2.tempo, 0) AS valor_tempo
        FROM historicoTrilha h2
        JOIN trilha t2
            ON t2.idTrilha = h2.idTrilha
    ) AS DISTINCT_CASE
        ON DISTINCT_CASE.idHistorico = h.idHistorico
    LEFT JOIN favorito f
        ON f.idUsuario = u.idUsuario
    LEFT JOIN avaliacao av
        ON av.idUsuario = u.idUsuario
    LEFT JOIN participante_evento pe
        ON pe.idUsuario = u.idUsuario
    WHERE u.idUsuario = p_id_usuario
    GROUP BY
        u.idUsuario,
        u.nome,
        u.email,
        u.fotoPerfil,
        u.dataCadastro;
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
        COUNT(DISTINCT h.idHistorico) AS trilhasConcluidas,
        ROUND(COALESCE(SUM(DISTINCT_CASE.valor_distancia), 0), 2) AS distanciaTotalKm,
        COUNT(DISTINCT av.idAvaliacao) AS avaliacoesRealizadas
    FROM usuario u
    LEFT JOIN historicoTrilha h
        ON h.idUsuario = u.idUsuario
    LEFT JOIN (
        SELECT
            h2.idHistorico,
            COALESCE(t2.distancia, 0) AS valor_distancia
        FROM historicoTrilha h2
        JOIN trilha t2
            ON t2.idTrilha = h2.idTrilha
    ) AS DISTINCT_CASE
        ON DISTINCT_CASE.idHistorico = h.idHistorico
    LEFT JOIN avaliacao av
        ON av.idUsuario = u.idUsuario
    GROUP BY
        u.idUsuario,
        u.nome,
        u.fotoPerfil
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
        ROUND(COALESCE(AVG(a.nota), 0), 2) AS mediaNota,
        COUNT(DISTINCT a.idAvaliacao) AS quantidadeAvaliacoes
    FROM favorito f
    JOIN trilha t
        ON t.idTrilha = f.idTrilha
    LEFT JOIN avaliacao a
        ON a.idTrilha = t.idTrilha
    WHERE f.idUsuario = p_id_usuario
    GROUP BY
        f.idFavorito,
        f.dataSalvo,
        t.idTrilha,
        t.nome,
        t.localizacao,
        t.distancia,
        t.dificuldade,
        t.tempoEstimadoMin,
        t.imagemUrl
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
        COUNT(DISTINCT pe.idUsuario) AS participantesAtuais,
        GROUP_CONCAT(DISTINCT t.nome ORDER BY t.nome SEPARATOR ', ') AS trilhas
    FROM evento e
    JOIN usuario u
        ON u.idUsuario = e.idCriador
    LEFT JOIN participante_evento pe
        ON pe.idEvento = e.idEvento
    LEFT JOIN evento_trilha et
        ON et.idEvento = e.idEvento
    LEFT JOIN trilha t
        ON t.idTrilha = et.idTrilha
    WHERE e.imediata = TRUE
       OR e.data IS NULL
       OR e.data >= CURRENT_DATE
    GROUP BY
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
        u.nome
    ORDER BY
        e.imediata DESC,
        e.data ASC,
        e.horarioSaida ASC,
        e.titulo ASC;
END$$

DELIMITER ;
