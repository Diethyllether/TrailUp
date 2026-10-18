# API TrailUp

Este serviço Flask é exclusivamente backend: registra endpoints JSON sob `/api` e não serve HTML, templates nem arquivos estáticos. O cliente é mantido separadamente em `../frontend` e pode ser hospedado em qualquer servidor de arquivos estáticos.

Para iniciar localmente:

```powershell
pip install -r requirements.txt
$env:DATABASE_URL = "mysql+pymysql://root:SENHA@localhost:3306/trilhas_db"
$env:SECRET_KEY = "defina-uma-chave-local"
$env:FRONTEND_ORIGIN = "http://localhost:8000"
python app.py
```

`FRONTEND_ORIGIN` controla a origem CORS permitida para o cliente, com credenciais habilitadas para sessão. Em produção com origens distintas, configure HTTPS, `SESSION_COOKIE_SAMESITE=None` e `SESSION_COOKIE_SECURE=true`.

Endpoints de aplicação: sessão/autenticação, trilhas, favoritos, eventos e avaliações. Consulte `api_controller.py`; as regras de negócio permanecem em `services/` e o acesso a dados em `repositories/`.
