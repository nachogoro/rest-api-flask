import time
from flask import Response
from flask_restx import Resource
from ..models import BookModel
from .. import db, api, app

class BookStream(Resource):
    @api.doc(
        description="Stream new books in real-time as they are added to the database."
    )
    def get(self):
        def generate():
            last_book_id = 0
            with app.app_context():  # Ensuring application context for database access
                while True:
                    new_books = BookModel.query.filter(BookModel.id > last_book_id).order_by(BookModel.id).all()
                    for book in new_books:
                        last_book_id = book.id
                        yield f'{{"id": {book.id}, "title": "{book.title}", "author": "{book.author}"}}\n'
                    time.sleep(2)

        return Response(generate(), mimetype='application/x-ndjson')
