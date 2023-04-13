import psycopg2
from flask import Flask
from .secret import settings

def create_app():
    app = Flask(__name__)
    try:
        db_user = settings.get('DATABASE_USER')
        db_pass = settings.get('DATABASE_PASSWORD')
        db_ip = settings.get('DATABASE_IP')
        db_port = settings.get('DATABASE_PORT')
        db_name = settings.get('DATABASE_NAME')
    except Exception as error:
        print(f"An unexpected error has occurred: {type(error)} -- {error}. Please try again.")

    from .models import Book, db
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_ip}:{db_port}/{db_name}"
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from . import library, main
    app.register_blueprint(library.blueprint)
    app.register_blueprint(main.blueprint)
    app.add_url_rule('/', endpoint='index')

    return app