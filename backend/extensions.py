"""
Instância única do SQLAlchemy, compartilhada por toda a aplicação.
Evita import circular entre app.py e os models.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
