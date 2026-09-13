"""Smoke test específico da migração Flutter -> Flask/Jinja2."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config as config_module

config_module.Config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
config_module.Config.TESTING = True
config_module.Config.GOOGLE_MAPS_API_KEY = ""

from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    db.create_all()

client = app.test_client()

# O site Jinja2 deve ser a entrada principal do produto.
r = client.get("/")
assert r.status_code == 200
assert b"TrailUp" in r.data

r = client.get("/mapa")
assert r.status_code == 200
assert "Expedições no mapa" in r.get_data(as_text=True)

# Cria dados suficientes para validar uma página real de trilha.
r = client.post(
    "/api/usuarios",
    json={"nome": "Web Tester", "email": "web@example.com", "senha": "senha123"},
)
assert r.status_code == 201

r = client.post("/api/login", json={"email": "web@example.com", "senha": "senha123"})
assert r.status_code == 200
headers = {"Authorization": f"Bearer {r.get_json()['token']}"}

r = client.post(
    "/api/trilhas",
    json={
        "nome": "Trilha Web",
        "localizacao": "Minas Gerais",
        "distancia": 5.0,
        "dificuldade": "MODERADA",
        "descricao": "Trilha usada para testar a versão web.",
    },
    headers=headers,
)
assert r.status_code == 201
id_trilha = r.get_json()["idTrilha"]

r = client.post(
    f"/api/trilhas/{id_trilha}/checkpoints",
    json={"latitude": -19.92, "longitude": -43.94},
    headers=headers,
)
assert r.status_code == 201

r = client.get(f"/trilhas/{id_trilha}")
assert r.status_code == 200
html = r.get_data(as_text=True)
assert "Trilha Web" in html
assert "Mapa da trilha" in html

# O download/registro de mapas offline foi retirado da API ativa.
r = client.post(
    f"/api/trilhas/{id_trilha}/mapas-offline",
    json={"arquivoUrl": "arquivo-legado.osm"},
    headers=headers,
)
assert r.status_code == 404

print("=== MIGRAÇÃO WEB VALIDADA ===")
