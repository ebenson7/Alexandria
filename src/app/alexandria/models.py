from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String, nullable=False)
    book_author = db.Column(db.String)
    book_publisher = db.Column(db.String)
    book_description = db.Column(db.String)