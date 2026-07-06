"""
Script auxiliar de desenvolvimento: cria as tabelas a partir dos models
atuais (útil depois de mudar um model, já que MySQL não migra schema
sozinho). Requer que o banco `trilhas_db` já exista no MySQL - rode
database/create_database.sql pelo menos uma vez antes (ele já cria o
banco e as tabelas; este script só recria tabelas que estejam faltando
a partir do metadata do SQLAlchemy).

Uso:
    python init_db.py
"""
from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Tabelas criadas/verificadas com sucesso em", app.config["SQLALCHEMY_DATABASE_URI"])
