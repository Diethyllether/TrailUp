from flask import Flask, jsonify

from config import Config
from extensions import db

import models    # noqa: F401

from controllers.usuario_controller import usuario_bp
from controllers.trilha_controller import trilha_bp
from controllers.avaliacao_controller import avaliacao_bp
from controllers.favorito_controller import favorito_bp
from controllers.checkpoint_controller import checkpoint_bp
from controllers.foto_controller import foto_bp
from controllers.mapa_offline_controller import mapa_offline_bp
from controllers.evento_controller import evento_bp
from controllers.notificacao_controller import notificacao_bp
from controllers.denuncia_controller import denuncia_bp
from controllers.historico_controller import historico_bp
from controllers.relatorio_controller import relatorio_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response

    blueprints = [
        usuario_bp,
        trilha_bp,
        avaliacao_bp,
        favorito_bp,
        checkpoint_bp,
        foto_bp,
        mapa_offline_bp,
        evento_bp,
        notificacao_bp,
        denuncia_bp,
        historico_bp,
        relatorio_bp,
    ]
    for bp in blueprints:
        app.register_blueprint(bp, url_prefix="/api")

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "service": "TrailUp API"}), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro": "recurso não encontrado"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"erro": "método não permitido para esta rota"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return jsonify({"erro": "erro interno do servidor"}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
