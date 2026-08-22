"""Teste focal do requisito de busca por nome ou localização.

Uso:
    cd backend
    python tests/requisitos_busca_test.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config as config_module

config_module.Config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    db.create_all()

client = app.test_client()

usuario = client.post(
    "/api/usuarios",
    json={"nome": "Teste", "email": "busca@trailup.test", "senha": "senha123"},
).get_json()

login = client.post(
    "/api/login",
    json={"email": "busca@trailup.test", "senha": "senha123"},
).get_json()
headers = {"Authorization": f"Bearer {login['token']}"}

client.post(
    "/api/trilhas",
    json={
        "nome": "Pico da Neblina",
        "localizacao": "Amazonas",
        "distancia": 12.0,
        "dificuldade": "DIFICIL",
    },
    headers=headers,
)
client.post(
    "/api/trilhas",
    json={
        "nome": "Serra do Cipó",
        "localizacao": "Minas Gerais",
        "distancia": 8.0,
        "dificuldade": "MODERADA",
    },
    headers=headers,
)

por_nome = client.get("/api/trilhas?busca=Neblina").get_json()
assert len(por_nome) == 1
assert por_nome[0]["nome"] == "Pico da Neblina"

por_localizacao = client.get("/api/trilhas?busca=Amazonas").get_json()
assert len(por_localizacao) == 1
assert por_localizacao[0]["localizacao"] == "Amazonas"

por_localizacao_parcial = client.get("/api/trilhas?busca=Minas").get_json()
assert len(por_localizacao_parcial) == 1
assert por_localizacao_parcial[0]["nome"] == "Serra do Cipó"

print("Busca por nome e localização: OK")
