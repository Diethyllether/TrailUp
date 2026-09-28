from sqlalchemy import or_
from sqlalchemy import func

from models.trilha_model import Trilha
from repositories.base_repository import BaseRepository

class TrilhaRepository(BaseRepository):
    """Consultas com filtros combinados. CRUD simples permanece na Model."""

    model = Trilha

    def buscar(self, nome=None, localizacao=None, dificuldade=None, busca=None):
        query = Trilha.query
        if busca:
            query = query.filter(
                or_(Trilha.nome.ilike(f"%{busca}%"), Trilha.localizacao.ilike(f"%{busca}%"))
            )
        if nome:
            query = query.filter(Trilha.nome.ilike(f"%{nome}%"))
        if localizacao:
            query = query.filter(Trilha.localizacao.ilike(f"%{localizacao}%"))
        if dificuldade:
            query = query.filter(Trilha.dificuldade == dificuldade)
        return query.all()

    def listar_ordenadas(self, ordenacao=None, distancia_max=None, duracao_max=None, nota_min=None):
        from models.avaliacao_model import Avaliacao
        query = Trilha.query.outerjoin(Avaliacao, Avaliacao.idTrilha == Trilha.idTrilha)
        query = query.group_by(Trilha.idTrilha)
        if distancia_max is not None:
            query = query.filter(Trilha.distancia <= distancia_max)
        if duracao_max is not None:
            query = query.filter(Trilha.duracao <= duracao_max)
        media = func.avg(Avaliacao.nota)
        if nota_min is not None:
            query = query.having(func.coalesce(media, 0) >= nota_min)
        coluna = {"distancia": Trilha.distancia, "duracao": Trilha.duracao, "nota": media}.get(ordenacao)
        if coluna is not None:
            ordem = coluna.desc() if ordenacao == "nota" else coluna.asc()
            query = query.order_by(coluna.is_(None).asc(), ordem)
        return query.all()

    def medias_avaliacao(self):
        from models.avaliacao_model import Avaliacao
        return dict(Trilha.query.outerjoin(Avaliacao, Avaliacao.idTrilha == Trilha.idTrilha)
                    .with_entities(Trilha.idTrilha, func.avg(Avaliacao.nota), func.count(Avaliacao.idAvaliacao))
                    .group_by(Trilha.idTrilha).all())

    def pontos_proximos(self):
        from models.checkpoint_model import Checkpoint
        return Checkpoint.query.filter(
            Checkpoint.latitude.between(-90, 90), Checkpoint.longitude.between(-180, 180),
            ~((Checkpoint.latitude == 0) & (Checkpoint.longitude == 0)),
        ).order_by(Checkpoint.idCheckpoint).all()
