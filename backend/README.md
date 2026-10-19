# API TrailUp

Este serviço Flask é exclusivamente backend: registra endpoints JSON sob `/api` e não serve HTML, templates nem arquivos estáticos. O cliente é mantido separadamente em `../frontend` e pode ser hospedado em qualquer servidor de arquivos estáticos.

Para iniciar localmente:

```powershell
pip install -r requirements.txt
Copy-Item .env.example .env
# Edite .env com a URL do banco e uma SECRET_KEY aleatória.
python app.py
```

`FRONTEND_ORIGIN` controla a origem CORS permitida para o cliente, com credenciais habilitadas para sessão. Em produção com origens distintas, configure HTTPS, `SESSION_COOKIE_SAMESITE=None` e `SESSION_COOKIE_SECURE=true`.

Endpoints de aplicação: sessão/autenticação, trilhas, favoritos, eventos, avaliações, recuperação de senha, ranking e resumo. A API usa Models para CRUD e repositories para consultas especializadas.
