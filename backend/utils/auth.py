"""
Autenticação sem dependências externas além do Flask:

- Hash de senha: werkzeug.security (já vem instalado junto com o Flask).
- Token de login: itsdangerous.URLSafeTimedSerializer (também já vem junto
  com o Flask — é a mesma lib que o Flask usa para assinar cookies de
  sessão). Não é um JWT "de mercado", mas cumpre o mesmo papel aqui: um
  token assinado, com validade, que não pode ser forjado sem o SECRET_KEY.
"""
from functools import wraps

from flask import request, jsonify, current_app
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash

def hash_senha(senha_plana: str) -> str:
    return generate_password_hash(senha_plana)

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return check_password_hash(senha_hash, senha_plana)

def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="trailup-auth")

def gerar_token(id_usuario: int) -> str:
    return _serializer().dumps({"id_usuario": id_usuario})

def token_obrigatorio(f):
    """Decorator de rota: exige um Bearer token válido e injeta id_usuario_logado."""

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"erro": "Token de autenticação ausente"}), 401

        token = auth_header.split(" ", 1)[1]
        max_age = current_app.config["TOKEN_EXP_MINUTES"] * 60
        try:
            dados = _serializer().loads(token, max_age=max_age)
        except SignatureExpired:
            return jsonify({"erro": "Token expirado"}), 401
        except BadSignature:
            return jsonify({"erro": "Token inválido"}), 401

        kwargs["id_usuario_logado"] = dados["id_usuario"]
        return f(*args, **kwargs)

    return decorated
