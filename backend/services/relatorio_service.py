from repositories.relatorio_repository import RelatorioRepository


class RelatorioService:
    def __init__(self):
        self.repository = RelatorioRepository()

    def trilhas_ordenadas(self, dificuldade=None, localizacao=None, ordem="nota"):
        ordens_validas = {"nota", "distancia", "nome"}
        if ordem not in ordens_validas:
            raise ValueError("ordem inválida; use nota, distancia ou nome")
        return self.repository.trilhas_ordenadas(
            dificuldade=dificuldade,
            localizacao=localizacao,
            ordem=ordem,
        )

    def favoritos_usuario(self, id_usuario):
        return self.repository.favoritos_usuario(id_usuario)

    def resumo_usuario(self, id_usuario):
        resumo = self.repository.resumo_usuario(id_usuario)
        if not resumo:
            raise ValueError("usuário não encontrado")
        return resumo

    def ranking_usuarios(self, limite=10):
        try:
            limite = int(limite)
        except (TypeError, ValueError):
            raise ValueError("limite deve ser um número inteiro")

        if limite < 1 or limite > 100:
            raise ValueError("limite deve estar entre 1 e 100")
        return self.repository.ranking_usuarios(limite)
