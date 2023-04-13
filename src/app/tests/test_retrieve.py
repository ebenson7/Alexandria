import pytest

from alexandria.models import db, Book
from flask_sqlalchemy import SQLAlchemy

def test_retrieve(client, app):
    assert client.get('/library/search').status_code == 200

    with app.app_context():
        test_list = list(db.session.execute(db.select(Book)).scalars())
        assert len(test_list) >= 1