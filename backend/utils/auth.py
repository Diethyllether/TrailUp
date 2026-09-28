from werkzeug.security import check_password_hash, generate_password_hash


def hash_senha(senha_plana: str) -> str:
    return generate_password_hash(senha_plana)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return check_password_hash(senha_hash, senha_plana)
