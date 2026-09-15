import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "mysql+pymysql://root:@localhost:3307/trilhas_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
    TOKEN_EXP_MINUTES = int(os.environ.get("TOKEN_EXP_MINUTES", "1440"))

    # Usada somente como mapa-base na visualização das trilhas. O traçado da
    # rota não vem da Directions API: ele é uma Polyline feita com os
    # checkpoints armazenados no banco do TrailUp.
    GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")

    DEBUG = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
