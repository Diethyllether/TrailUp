USE trilhas_db;

DROP PROCEDURE IF EXISTS sp_trilhas_por_dificuldade;
DROP PROCEDURE IF EXISTS sp_resumo_usuario;
DROP PROCEDURE IF EXISTS sp_ranking_usuarios;

DELIMITER $$

CREATE PROCEDURE sp_trilhas_por_dificuldade(
    IN p_dificuldade VARCHAR(50)
)
BEGIN
    SELECT t.idTrilha,
           t.nome,
           t.localizacao,
           t.distancia,
           t.dificuldade,
           ROUND(COALESCE(AVG(a.nota), 0), 2) AS mediaNota,
           COUNT(a.idAvaliacao) AS quantidadeAvaliacoes
      FROM trilha t
 LEFT JOIN avaliacao a ON a.idTrilha = t.idTrilha
     WHERE p_dificuldade IS NULL OR t.dificuldade = p_dificuldade
  GROUP BY t.idTrilha, t.nome, t.localizacao, t.distancia, t.dificuldade
  ORDER BY mediaNota DESC, quantidadeAvaliacoes DESC, t.nome ASC;
END$$

CREATE PROCEDURE sp_resumo_usuario(
    IN p_id_usuario INT
)
BEGIN
    SELECT u.idUsuario,
           u.nome,
           u.email,
           COUNT(DISTINCT h.idHistorico) AS trilhasRealizadas,
           COUNT(DISTINCT f.idFavorito) AS totalFavoritos,
           COUNT(DISTINCT av.idAvaliacao) AS totalAvaliacoes,
           ROUND(COALESCE(AVG(av.nota), 0), 2) AS mediaNotasDadas
      FROM usuario u
 LEFT JOIN historicoTrilha h ON h.idUsuario = u.idUsuario
 LEFT JOIN favorito f ON f.idUsuario = u.idUsuario
 LEFT JOIN avaliacao av ON av.idUsuario = u.idUsuario
     WHERE u.idUsuario = p_id_usuario
  GROUP BY u.idUsuario, u.nome, u.email;
END$$

CREATE PROCEDURE sp_ranking_usuarios(
    IN p_limite INT
)
BEGIN
    SELECT u.idUsuario,
           u.nome,
           COUNT(DISTINCT h.idHistorico) AS trilhasConcluidas,
           COUNT(DISTINCT av.idAvaliacao) AS avaliacoesRealizadas
      FROM usuario u
 LEFT JOIN historicoTrilha h ON h.idUsuario = u.idUsuario
 LEFT JOIN avaliacao av ON av.idUsuario = u.idUsuario
  GROUP BY u.idUsuario, u.nome
  ORDER BY trilhasConcluidas DESC, avaliacoesRealizadas DESC, u.nome ASC
     LIMIT p_limite;
END$$

DELIMITER ;
