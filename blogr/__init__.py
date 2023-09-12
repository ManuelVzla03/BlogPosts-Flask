from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
import locale

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")
    db.init_app(app)
    ckeditor = CKEditor(app)
    locale.setlocale(locale.LC_ALL, 'es_ES')

    from blogr import home
    app.register_blueprint(home.bp)
    from blogr import auth
    app.register_blueprint(auth.bp)
    from blogr import post
    app.register_blueprint(post.bp)

    from .models import User, Post

    with app.app_context():
        db.create_all()

    return app
