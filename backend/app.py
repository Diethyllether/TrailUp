from pathlib import Path

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from config import Config

import models

from controllers.web_controller import web_bp


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
db = SQLAlchemy()


def create_app():
    app = Flask(
        __name__,
        template_folder=str(FRONTEND_DIR / "templates"),
        static_folder=str(FRONTEND_DIR / "static"),
    )
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    db.init_app(app)
    app.register_blueprint(web_bp)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html", usuario_logado=None), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return render_template("404.html", usuario_logado=None), 405

    @app.errorhandler(500)
    def internal_error(_error):
        db.session.rollback()
        app.logger.exception("Web request failed")
        return render_template("500.html", usuario_logado=None), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
