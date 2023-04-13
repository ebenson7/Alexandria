from flask import Blueprint, render_template, request, url_for, redirect
from isbnlib import isbn_from_words, desc, meta
from alexandria.models import db, Book
from flask_sqlalchemy import SQLAlchemy

blueprint = Blueprint('library', __name__, url_prefix="/library/")

def getBookISBN(title: str, author: str) -> int:
    isbn = isbn_from_words(f"{title} {author}")
    return isbn

def populateData(isbn: int, author: str, publisher: str) -> str:
    """
    Uses isbnlib to retrieve information that may have been unknown or left out.

    Currently, OpenLibrary gives the most concise information so that is the service we can query. We can also use Google Books or Wikipedia if needed.

    isbn: int
    author: str
    publisher: str
    """

    description = desc(isbn)
    if not publisher:
        publisher = meta(isbn, service="openl")['Publisher'].title()

    if not author:
        author = meta(isbn, service="openl")['Authors']
        if len(author) == 1:
            author = author[0].title()
        elif len(author) >= 2:
            author = ', '.join(author).title()

    return author, publisher, description

@blueprint.post("/insert")
def insertItem():
    isbn = isbn_from_words(f"{request.form['book_title']} {request.form['book_author']}")
    auth, pub, des = populateData(isbn, request.form['book_author'], request.form['book_publisher'])
    print(auth)
    try:
        test_book = Book(
            book_title=request.form["book_title"].title(),
            book_author=auth,
            book_publisher=pub,
            book_description=des
        )
        db.session.add(test_book)
        db.session.commit()
        return redirect(url_for('library.getItem'))
    except Exception as error:
        pass


@blueprint.route("/search")
def getItem():
    test = list(db.session.execute(db.select(Book)).scalars())
    return render_template("search.html", books=test)