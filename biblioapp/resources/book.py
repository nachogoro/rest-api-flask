from flask import request
from flask_restx import Resource
from ..models import BookModel
from ..auth import token_required
from .. import db, api

class Book(Resource):
    @api.doc(description="Retrieve a book by its ID.")
    @api.marshal_with(api.models['Book'])
    def get(self, book_id):
        book = BookModel.query.get(book_id)
        if not book:
            return {"error": "Book not found"}, 404
        return {"id": book.id, "title": book.title, "author": book.author}

    @api.expect(api.models['BookInput'])
    @token_required
    def put(self, book_id):
        book = BookModel.query.get(book_id)
        if not book:
            return {"error": "Book not found"}, 404

        updated_data = request.json
        book.title = updated_data.get('title', book.title)
        book.author = updated_data.get('author', book.author)
        db.session.commit()
        return {"id": book.id, "title": book.title, "author": book.author}

    @token_required
    def delete(self, book_id):
        book = BookModel.query.get(book_id)
        if not book:
            return {"error": "Book not found"}, 404
        db.session.delete(book)
        db.session.commit()
        return '', 204
