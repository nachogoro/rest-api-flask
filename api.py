import math
import time
from collections import defaultdict
from datetime import datetime, timedelta

from flask import Flask, request, Response, jsonify, make_response
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

authorizations = {
    'BearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter your Bearer token in the format **Bearer <token>**'
    }
}

api = Api(app, authorizations=authorizations, security='BearerAuth', doc='/api/v1')
v1 = api.namespace('api/v1', description='Version 1 of the API')

# API model of a book in a response
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

# API model of a book in a request
book_input_model = api.model('BookInput', {
    'title': fields.String(required=True, description='The title of the book', example='1984'),
    'author': fields.String(required=True, description='The author of the book', example='George Orwell')
})


# Database model for books
class BookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)


# Sample bearer token for demonstration
VALID_TOKEN = "Bearer mysecrettoken"

request_counts = defaultdict(list)


# Decorator for authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or auth_header != VALID_TOKEN:
            return {"error": "Invalid token, check your Authorization header"}, 401

        # Rate limiting: allow 100 requests per token per minute
        max_requests = 100
        sliding_window_width = timedelta(seconds=60)
        current_time = datetime.now()

        with request_lock:
            # Timestamps of processed requests for this token in the last window
            request_times = [t for t in request_counts[auth_header]
                             if current_time - t < sliding_window_width]

            remaining_requests = max(max_requests - len(request_times), 0)
            since_oldest_request = (current_time - (request_times[0] if request_times else current_time))
            reset_delta = sliding_window_width - since_oldest_request
            if remaining_requests > 0:
                # If the request will be processed add its timestamp to the list of handled requests
                request_times.append(current_time)
            request_counts[auth_header] = request_times

        if remaining_requests <= 0:
            response = jsonify({"error": "Rate limit exceeded, wait for reset"})
            response.status_code = 429
            response.headers['RateLimit-Limit'] = str(max_requests)
            response.headers['RateLimit-Remaining'] = '0'
            response.headers['RateLimit-Reset'] = str(reset_delta.total_seconds())
            return response

        response = f(*args, **kwargs)

        # Ensure response is a Response object
        if not isinstance(response, Response):
            response = make_response(response)

        response.headers['RateLimit-Limit'] = str(max_requests)
        response.headers['RateLimit-Remaining'] = str(remaining_requests - 1)
        response.headers['RateLimit-Reset'] = str(reset_delta.total_seconds())

        return response

    return decorated


@v1.route('/books')
class BookList(Resource):
    @api.doc(
        description="Retrieve a list of books with optional filters and pagination.",
        params={
            'title': 'Filter books by title.',
            'author': 'Filter books by author.',
            'sort': 'Comma-separated list of fields to sort by (e.g., "+title,-author").',
            'page': 'Page number for pagination.',
            'per_page': 'Number of books per page for pagination.'
        }
    )
    @api.marshal_with(book_list_response_model)
    def get(self):
        """
        Get a list of books with optional filters, sorting, and pagination.
        """
        title_filter = request.args.get('title')
        author_filter = request.args.get('author')
        sort_by = request.args.get('sort', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        query = BookModel.query

        # Filter by title if provided
        if title_filter:
            query = query.filter(BookModel.title.ilike(f"%{title_filter}%"))

        # Filter by author if provided
        if author_filter:
            query = query.filter(BookModel.author.ilike(f"%{author_filter}%"))

        # Sort if sort_by is provided
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

            # Apply all sort fields at once to the query
            if sort_fields:
                query = query.order_by(*sort_fields)

        # Pagination
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
    @api.doc(
        description="Add a new book to the collection.",
        security="BearerAuth",
        responses={
            201: 'Book created successfully.',
            400: 'Invalid input: Missing required fields.',
            423: 'Rate limit exceeded.'
        }
    )
    @token_required
    def post(self):
        new_book_data = request.json
        if not new_book_data.get('title') or not new_book_data.get('author'):
            return {"error": "Missing required book fields (title, author)"}, 400

        new_book = BookModel(title=new_book_data['title'], author=new_book_data['author'])
        db.session.add(new_book)
        db.session.commit()
        return {"id": new_book.id, "title": new_book.title, "author": new_book.author}, 201


@v1.route('/books/<int:book_id>')
@api.doc(params={'book_id': 'The ID of the book to retrieve or modify.'})
class Book(Resource):
    @api.doc(
        description="Retrieve a book by its ID.",
        responses={
            200: 'Success',
            404: 'Book not found'
        }
    )
    @api.marshal_with(book_model)
    def get(self, book_id):
        book = BookModel.query.get(book_id)
        if not book:
            return {"error": "Book not found"}, 404
        return {"id": book.id, "title": book.title, "author": book.author}

    @api.expect(book_input_model)
    @api.doc(
        description="Update a book's information.",
        security="BearerAuth",
        responses={
            200: 'Book updated successfully.',
            400: 'Invalid input: Missing required fields.',
            404: 'Book not found',
            429: 'Rate limit exceeded.'
        }
    )
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

    @api.doc(
        description="Delete a book by its ID.",
        security="BearerAuth",
        responses={
            204: 'Book deleted successfully.',
            404: 'Book not found',
            429: 'Rate limit exceeded.'
        }
    )
    @token_required
    def delete(self, book_id):
        book = BookModel.query.get(book_id)
        if not book:
            return {"error": "Book not found"}, 404
        db.session.delete(book)
        db.session.commit()
        return '', 204


@v1.route('/books/stream')
class BookStream(Resource):
    @api.doc(
        description="Stream new books in real-time as they are added to the database. Each line "
                    "in the response is a JSON object representing a book.",
        responses={
            200: 'Stream started successfully',
        }
    )
    def get(self):
        def generate():
            with app.app_context():
                last_book_id = 0
                while True:
                    new_books = BookModel.query.filter(BookModel.id > last_book_id).order_by(
                        BookModel.id).all()
                    for book in new_books:
                        last_book_id = book.id
                        yield f'{{"id": {book.id}, "title": "{book.title}", "author": "{book.author}"}}\n'
                    time.sleep(2)

        return Response(generate(), mimetype='application/x-ndjson')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
