import pytest
from alexandria import create_app
from alexandria.models import db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"postgresql+psycopg2://{db_user}:{db_pass}@{db_ip}:{db_port}/testing"
    })

    with app.test_request_context():
        class test_db(db.Model):
            __tablename__ = "test_db"
            book_id = db.Column(db.Integer, primary_key=True)
            book_title = db.Column(db.String, nullable=False)
            book_author = db.Column(db.String)
            book_publisher = db.Column(db.String)
            book_description = db.Column(db.String)

            db.init_app(app)
            db.create_all()

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()