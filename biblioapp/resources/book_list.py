from flask import request
from flask_restx import Resource
from ..models import BookModel
from ..auth import token_required
from .. import db, api
from flask_restx import fields
import math

book_model = api.model('Book', {
    'id': fields.Integer(description='The unique identifier of the book', example=1),
    'title': fields.String(required=True, description='The title of the book', example='1984'),
    'author': fields.String(required=True, description='The author of the book', example='George Orwell')
})

book_list_response_model = api.model('BookListResponse', {
    'page': fields.Integer(description='The current page number'),
    'per_page': fields.Integer(description='The number of books per page'),
    'total_pages': fields.Integer(description='The total number of pages'),
    'total_books': fields.Integer(description='The total number of books'),
    'books': fields.List(fields.Nested(book_model), description='The list of books')
})

book_input_model = api.model('BookInput', {
    'title': fields.String(required=True, description='The title of the book', example='1984'),
    'author': fields.String(required=True, description='The author of the book', example='George Orwell')
})

class BookList(Resource):
    @api.doc(description="Retrieve a list of books with optional filters and pagination.")
    @api.marshal_with(book_list_response_model)
    def get(self):
        title_filter = request.args.get('title')
        author_filter = request.args.get('author')
        sort_by = request.args.get('sort', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        query = BookModel.query
        if title_filter:
            query = query.filter(BookModel.title.ilike(f"%{title_filter}%"))
        if author_filter:
            query = query.filter(BookModel.author.ilike(f"%{author_filter}%"))

        if sort_by:
            sort_keys = sort_by.split(',')
            sort_fields = []
            for key in sort_keys:
                reverse = key.startswith('-')
                field = key.lstrip('+-')
                if field in ['title', 'author']:
                    sort_field = getattr(BookModel, field)
                    if reverse:
                        sort_field = sort_field.desc()
                    sort_fields.append(sort_field)
            if sort_fields:
                query = query.order_by(*sort_fields)

        total_books = query.count()
        books = query.offset((page - 1) * per_page).limit(per_page).all()
        total_pages = math.ceil(total_books / per_page)

        result = [{"id": book.id, "title": book.title, "author": book.author} for book in books]
        return {
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_books": total_books,
            "books": result
        }

    @api.expect(book_input_model)
    @token_required
    def post(self):
        new_book_data = request.json
        if not new_book_data.get('title') or not new_book_data.get('author'):
            return {"error": "Missing required book fields (title, author)"}, 400

        new_book = BookModel(title=new_book_data['title'], author=new_book_data['author'])
        db.session.add(new_book)
        db.session.commit()
        return {"id": new_book.id, "title": new_book.title, "author": new_book.author}, 201
