import unicodedata


def normalizar_dificuldade(valor):
    if not valor:
        return valor
    sem_acento = unicodedata.normalize("NFKD", valor).encode("ascii", "ignore").decode()
    codigo = sem_acento.strip().upper()
    if codigo in ("MODERADO", "MODERADA"):
        return "MODERADA"
    if codigo in ("FACIL", "DIFICIL"):
        return codigo
    return valor
