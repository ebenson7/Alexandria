import pytest

from alexandria.models import db, Book
from flask_sqlalchemy import SQLAlchemy

def test_insert(client, app):
    with app.app_context():
        class test_db(db.Model):
            __tablename__ = "test_db"
            book_id = db.Column(db.Integer, primary_key=True)
            book_title = db.Column(db.String, nullable=False)
            book_author = db.Column(db.String)
            book_publisher = db.Column(db.String)
            book_description = db.Column(db.String)

        test_book = test_db(
            book_title="Book from Pytest",
            book_author="Pytest",
            book_publisher="Pytest Publishing",
            book_description="This is a test from Pytest"
        )
        db.session.add(test_book)
        db.session.commit()
        db.session.rollback()
        db.session.close()
        test_db.__table__.drop(db.engine)