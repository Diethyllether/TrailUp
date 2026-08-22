import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "mysql+pymysql://root:@localhost:3307/trilhas_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
    TOKEN_EXP_MINUTES = int(os.environ.get("TOKEN_EXP_MINUTES", "1440"))

    DEBUG = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
