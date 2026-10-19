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
        COALESCE(av.mediaNota, 0) AS mediaNota,
        COALESCE(av.quantidadeAvaliacoes, 0) AS quantidadeAvaliacoes,
        COALESCE(fav.quantidadeFavoritos, 0) AS quantidadeFavoritos,
        COALESCE(hist.quantidadeConclusoes, 0) AS quantidadeConclusoes
    FROM trilha t
    LEFT JOIN (
        SELECT
            idTrilha,
            ROUND(AVG(nota), 2) AS mediaNota,
            COUNT(*) AS quantidadeAvaliacoes
        FROM avaliacao
        GROUP BY idTrilha
    ) av ON av.idTrilha = t.idTrilha
    LEFT JOIN (
        SELECT
            idTrilha,
            COUNT(*) AS quantidadeFavoritos
        FROM favorito
        GROUP BY idTrilha
    ) fav ON fav.idTrilha = t.idTrilha
    LEFT JOIN (
        SELECT
            idTrilha,
            COUNT(*) AS quantidadeConclusoes
        FROM historicoTrilha
        GROUP BY idTrilha
    ) hist ON hist.idTrilha = t.idTrilha
    WHERE p_dificuldade IS NULL
       OR p_dificuldade = ''
       OR t.dificuldade = p_dificuldade
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

DELIMITER ;
