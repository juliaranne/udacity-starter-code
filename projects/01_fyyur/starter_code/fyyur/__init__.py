import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'), static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))
    app.config.from_object('config')
    app.app_context().push()

    db.init_app(app)
    migrate = Migrate(app, db)

    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
