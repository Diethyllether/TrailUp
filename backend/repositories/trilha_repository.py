from sqlalchemy import or_

from models.trilha_model import Trilha

class TrilhaRepository:
    """Consultas com filtros combinados. CRUD simples permanece na Model."""

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
