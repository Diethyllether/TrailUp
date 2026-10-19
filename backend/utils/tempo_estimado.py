VELOCIDADE_POR_DIFICULDADE = {
    "FACIL": 4.0,
    "MODERADA": 3.0,
    "DIFICIL": 2.0,
}


def calcular_tempo_estimado_min(distancia_km, dificuldade):
    if not distancia_km:
        return None
    velocidade = VELOCIDADE_POR_DIFICULDADE.get((dificuldade or "").upper(), 3.0)
    return round(distancia_km / velocidade * 60, 1)
