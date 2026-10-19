from functools import wraps

from flask import session

from utils.excecoes import NaoAutenticado


def login_obrigatorio(funcao):
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        if not session.get("id_usuario"):
            raise NaoAutenticado("Autenticação necessária")
        return funcao(*args, **kwargs)

    return wrapper
