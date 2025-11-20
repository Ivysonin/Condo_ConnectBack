from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp, url_prefix="/users")

    from app.models import user_model, chamado_model, aviso_model

    return app