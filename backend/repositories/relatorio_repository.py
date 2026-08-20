from sqlalchemy import text

from extensions import db


class RelatorioRepository:
    def trilhas_ordenadas(self, dificuldade=None, localizacao=None, ordem="nota"):
        ordenacoes = {
            "nota": "mediaNota DESC, quantidadeAvaliacoes DESC, t.nome ASC",
            "distancia": "t.distancia ASC, t.nome ASC",
            "nome": "t.nome ASC",
        }
        order_by = ordenacoes.get(ordem, ordenacoes["nota"])
        localizacao_like = f"%{localizacao}%" if localizacao else None

        sql = f"""
            SELECT t.idTrilha, t.nome, t.localizacao, t.distancia,
                   t.dificuldade, t.tempoEstimadoMin,
                   ROUND(COALESCE(AVG(a.nota), 0), 2) AS mediaNota,
                   COUNT(a.idAvaliacao) AS quantidadeAvaliacoes
              FROM trilha t
         LEFT JOIN avaliacao a ON a.idTrilha = t.idTrilha
             WHERE (:dificuldade IS NULL OR t.dificuldade = :dificuldade)
               AND (:localizacao_like IS NULL OR t.localizacao LIKE :localizacao_like)
          GROUP BY t.idTrilha, t.nome, t.localizacao, t.distancia,
                   t.dificuldade, t.tempoEstimadoMin
          ORDER BY {order_by}
        """
        return [dict(linha._mapping) for linha in db.session.execute(
            text(sql), {
                "dificuldade": dificuldade,
                "localizacao_like": localizacao_like,
            }
        )]

    def favoritos_usuario(self, id_usuario):
        sql = text("""
            SELECT f.idFavorito, f.dataSalvo, t.idTrilha, t.nome,
                   t.localizacao, t.dificuldade,
                   ROUND(COALESCE(AVG(a.nota), 0), 2) AS mediaNota
              FROM favorito f
              JOIN trilha t ON t.idTrilha = f.idTrilha
         LEFT JOIN avaliacao a ON a.idTrilha = t.idTrilha
             WHERE f.idUsuario = :id_usuario
          GROUP BY f.idFavorito, f.dataSalvo, t.idTrilha, t.nome,
                   t.localizacao, t.dificuldade
          ORDER BY f.dataSalvo DESC, t.nome ASC
        """)
        return [dict(linha._mapping) for linha in db.session.execute(
            sql, {"id_usuario": id_usuario}
        )]

    def resumo_usuario(self, id_usuario):
        sql = text("""
            SELECT u.idUsuario, u.nome, u.email,
                   COUNT(DISTINCT h.idHistorico) AS trilhasRealizadas,
                   COUNT(DISTINCT f.idFavorito) AS totalFavoritos,
                   COUNT(DISTINCT av.idAvaliacao) AS totalAvaliacoes,
                   ROUND(COALESCE(AVG(av.nota), 0), 2) AS mediaNotasDadas
              FROM usuario u
         LEFT JOIN historicoTrilha h ON h.idUsuario = u.idUsuario
         LEFT JOIN favorito f ON f.idUsuario = u.idUsuario
         LEFT JOIN avaliacao av ON av.idUsuario = u.idUsuario
             WHERE u.idUsuario = :id_usuario
          GROUP BY u.idUsuario, u.nome, u.email
        """)
        linha = db.session.execute(sql, {"id_usuario": id_usuario}).first()
        return dict(linha._mapping) if linha else None

    def ranking_usuarios(self, limite=10):
        sql = text("""
            SELECT u.idUsuario, u.nome,
                   COUNT(DISTINCT h.idHistorico) AS trilhasConcluidas,
                   COUNT(DISTINCT av.idAvaliacao) AS avaliacoesRealizadas
              FROM usuario u
         LEFT JOIN historicoTrilha h ON h.idUsuario = u.idUsuario
         LEFT JOIN avaliacao av ON av.idUsuario = u.idUsuario
          GROUP BY u.idUsuario, u.nome
          ORDER BY trilhasConcluidas DESC, avaliacoesRealizadas DESC, u.nome ASC
             LIMIT :limite
        """)
        return [dict(linha._mapping) for linha in db.session.execute(
            sql, {"limite": limite}
        )]
