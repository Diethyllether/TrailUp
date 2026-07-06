"""
Smoke test: sobe a API inteira com SQLite em memória (não precisa de MySQL
rodando) e exercita os principais fluxos ponta a ponta. Serve para validar
a lógica de controllers/services/repositories sem depender de infra.

Uso:
    cd backend
    python tests/smoke_test.py
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

def show(label, resp):
    print(f"\n--- {label} [{resp.status_code}] ---")
    print(resp.get_json())
    return resp.get_json()

r = show("cadastro usuario 1", client.post("/api/usuarios", json={
    "nome": "Ana Trilheira", "email": "ana@example.com", "senha": "senha123"
}))
assert r["email"] == "ana@example.com"

r2 = show("cadastro usuario 2 (líder)", client.post("/api/usuarios", json={
    "nome": "Bruno Guia", "email": "bruno@example.com", "senha": "senha123"
}))

r = show("login", client.post("/api/login", json={"email": "ana@example.com", "senha": "senha123"}))
assert "token" in r
token = r["token"]
headers = {"Authorization": f"Bearer {token}"}

r = show("login bruno", client.post("/api/login", json={"email": "bruno@example.com", "senha": "senha123"}))
token_bruno = r["token"]
headers_bruno = {"Authorization": f"Bearer {token_bruno}"}

uid = r2["idUsuario"]
r = show("editar perfil (deve falhar - outro usuario)", client.put(f"/api/usuarios/{uid}", json={"nome": "x"}, headers=headers))
assert r["erro"]

r = show("criar trilha", client.post("/api/trilhas", json={
    "nome": "Pico da Neblina",
    "localizacao": "Amazonas",
    "distancia": 12.0,
    "dificuldade": "DIFICIL",
    "descricao": "Trilha difícil na Amazônia",
}, headers=headers))
assert r["tempoEstimadoMin"] == 360.0
id_trilha = r["idTrilha"]

r = show("buscar trilha por nome", client.get("/api/trilhas?nome=Neblina"))
assert len(r) == 1

r = show("filtrar por dificuldade errada", client.get("/api/trilhas?dificuldade=FACIL"))
assert len(r) == 0

r = show("favoritar trilha", client.post("/api/favoritos", json={"idTrilha": id_trilha}, headers=headers))
assert r["idTrilha"] == id_trilha

r_ana_fav = show("listar favoritos ana", client.get(f"/api/usuarios/1/favoritos", headers=headers))
assert len(r_ana_fav) == 1

r = show("avaliar trilha", client.post(f"/api/trilhas/{id_trilha}/avaliacoes", json={
    "nota": 5, "comentario": "Trilha incrível!"
}, headers=headers))
assert r["nota"] == 5

show("criar checkpoint", client.post(f"/api/trilhas/{id_trilha}/checkpoints", json={
    "latitude": -0.795, "longitude": -62.99
}, headers=headers))

show("criar foto da trilha", client.post(f"/api/trilhas/{id_trilha}/fotos", json={
    "url": "https://cdn.trailup.com/fotos/1.jpg", "legenda": "Vista do topo"
}, headers=headers))

show("registrar mapa offline", client.post(f"/api/trilhas/{id_trilha}/mapas-offline", json={
    "arquivoUrl": "https://cdn.trailup.com/mapas/1.osm", "tamanhoArquivo": 15.4
}, headers=headers))

r = show("criar evento (sala)", client.post("/api/eventos", json={
    "titulo": "Saindo agora!", "tipo": "GRUPO", "vagas": 5,
    "imediata": True, "latitude": -0.80, "longitude": -63.0,
    "trilhas": [id_trilha],
}, headers=headers_bruno))
id_evento = r["idEvento"]

r = show("listar eventos no mapa", client.get("/api/eventos?mapa=true"))
assert len(r) == 1

show("ana entra na sala", client.post(f"/api/eventos/{id_evento}/entrar", json={}, headers=headers))
r = show("listar participantes", client.get(f"/api/eventos/{id_evento}/participantes"))
assert len(r) == 2

r = show("denunciar comportamento", client.post(f"/api/eventos/{id_evento}/denuncias", json={
    "descricao": "Comportamento inadequado durante a trilha"
}, headers=headers))
id_denuncia = r["idDenuncia"]

r = show("moderação atualiza status", client.put(f"/api/denuncias/{id_denuncia}/status", json={"status": "EM_ANALISE"}, headers=headers))
assert r["status"] == "EM_ANALISE"

r = show("criar notificacao", client.post("/api/notificacoes", json={
    "idUsuario": 1, "mensagem": "Sua sala está quase cheia!", "idEvento": id_evento
}, headers=headers))
id_notif = r["idNotificacao"]
r = show("marcar notificacao como lida", client.put(f"/api/notificacoes/{id_notif}/lida", headers=headers))
assert r["lida"] is True

r = show("registrar historico", client.post("/api/historico", json={
    "idTrilha": id_trilha, "idEvento": id_evento, "tempo": 340.5, "avaliacaoPessoal": 5
}, headers=headers))
id_historico = r["idHistorico"]

r = show("registrar checkpoint GPS", client.post(f"/api/historico/{id_historico}/registros", json={
    "latitude": -0.796, "longitude": -62.991, "observacao": "Checkpoint 1"
}, headers=headers))
id_registro = r["idRegistro"]

show("anexar foto ao registro", client.post(f"/api/registros/{id_registro}/fotos", json={
    "url": "https://cdn.trailup.com/registros/1.jpg", "legenda": "No checkpoint"
}, headers=headers))

r = show("listar historico da ana", client.get("/api/usuarios/1/historico", headers=headers))
assert len(r) == 1

r = show("solicitar recuperacao senha", client.post("/api/recuperar-senha", json={"email": "ana@example.com"}))
token_reset = r["token_debug"]
show("redefinir senha", client.post("/api/redefinir-senha", json={"token": token_reset, "novaSenha": "novaSenha456"}))

r = show("login com senha antiga (deve falhar)", client.post("/api/login", json={"email": "ana@example.com", "senha": "senha123"}))
assert r["erro"]

r = show("login com senha nova", client.post("/api/login", json={"email": "ana@example.com", "senha": "novaSenha456"}))
assert "token" in r

r = show("health check", client.get("/api/health"))
assert r["status"] == "ok"

print("\n\n=== TODOS OS TESTES PASSARAM ===")
