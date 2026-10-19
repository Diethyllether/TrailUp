from flask import Flask, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from config import Config
from extensions import db
import models
from routes.relatorio_routes import relatorio_bp
from routes.auth_routes import auth_bp
from routes.usuario_routes import usuario_bp
from routes.trilha_routes import trilha_bp
from routes.favorito_routes import favorito_bp
from routes.evento_routes import evento_bp
from routes.avaliacao_routes import avaliacao_bp
from routes.historico_routes import historico_bp
from routes.checklist_routes import checklist_bp
from routes.denuncia_routes import denuncia_bp
from routes.termo_routes import termo_bp
from utils.excecoes import ErroDeDominio


def create_app():
    # This process exposes JSON endpoints only. The frontend is hosted separately.
    app = Flask(__name__, static_folder=None)
    Config.validar()
    app.config.from_object(Config)
    app.url_map.strict_slashes = False
    db.init_app(app)
    for blueprint in (
        auth_bp,
        usuario_bp,
        trilha_bp,
        favorito_bp,
        evento_bp,
        avaliacao_bp,
        historico_bp,
        checklist_bp,
        denuncia_bp,
        relatorio_bp,
        termo_bp,
    ):
        prefix = "" if blueprint is termo_bp else "/api"
        app.register_blueprint(blueprint, url_prefix=prefix)

    @app.after_request
    def api_cors(response):
        origin = request.headers.get("Origin")
        allowed_origin = Config.FRONTEND_ORIGIN
        if origin == allowed_origin:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Vary"] = "Origin"
        if request.method == "OPTIONS":
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Access-Control-Max-Age"] = "600"
        return response

    @app.route("/api", methods=["OPTIONS"])
    @app.route("/api/<path:_path>", methods=["OPTIONS"])
    def options(_path=None):
        return "", 204

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify(error="Recurso da API não encontrado"), 404

    @app.errorhandler(500)
    def internal_error(_error):
        db.session.rollback()
        app.logger.exception("API request failed")
        return jsonify(error="Erro interno do servidor"), 500

    @app.errorhandler(ErroDeDominio)
    def erro_de_dominio(error):
        return jsonify(error=error.mensagem), error.status_http

    @app.errorhandler(SQLAlchemyError)
    def erro_de_banco(error):
        db.session.rollback()
        app.logger.exception("Falha de persistência na API", exc_info=error)
        return jsonify(error="Erro ao acessar o banco de dados"), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
