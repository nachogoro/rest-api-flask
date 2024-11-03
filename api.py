from flask import Flask, request
from flask_restx import Api, Resource
from functools import wraps

app = Flask(__name__)
api = Api(app)

# In-memory storage for demonstration purposes
# Not thread-safe or process-safe!
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen"},
    {"id": 5, "title": "Moby Dick", "author": "Herman Melville"},
    {"id": 6, "title": "War and Peace", "author": "Leo Tolstoy"},
    {"id": 7, "title": "The Catcher in the Rye", "author": "J.D. Salinger"},
    {"id": 8, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"id": 9, "title": "Ulysses", "author": "James Joyce"},
    {"id": 10, "title": "The Odyssey", "author": "Homer"},
    {"id": 11, "title": "Crime and Punishment", "author": "Fyodor Dostoevsky"},
    {"id": 12, "title": "Brave New World", "author": "Aldous Huxley"},
    {"id": 13, "title": "The Divine Comedy", "author": "Dante Alighieri"},
    {"id": 14, "title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky"},
    {"id": 15, "title": "Anna Karenina", "author": "Leo Tolstoy"},
    {"id": 16, "title": "One Hundred Years of Solitude", "author": "Gabriel Garcia Marquez"},
    {"id": 17, "title": "Wuthering Heights", "author": "Emily Bronte"},
    {"id": 18, "title": "Great Expectations", "author": "Charles Dickens"},
    {"id": 19, "title": "The Iliad", "author": "Homer"},
    {"id": 20, "title": "Jane Eyre", "author": "Charlotte Bronte"},
    {"id": 21, "title": "A Tale of Two Cities", "author": "Charles Dickens"},
    {"id": 22, "title": "The Great Adventure", "author": "Leo Tolstoy"},
    {"id": 23, "title": "The Shadow and the Wind", "author": "Carlos Ruiz Zafon"},
    {"id": 24, "title": "The Great Wave", "author": "Hokusai"},
    {"id": 25, "title": "The Wind-Up Bird Chronicle", "author": "Haruki Murakami"},
    {"id": 26, "title": "Norwegian Wood", "author": "Haruki Murakami"},
    {"id": 27, "title": "Kafka on the Shore", "author": "Haruki Murakami"},
    {"id": 28, "title": "The Brothers", "author": "Fyodor Dostoevsky"},
    {"id": 29, "title": "The Great Sea", "author": "David Abulafia"},
    {"id": 30, "title": "The Catcher of Tales", "author": "Leo Tolstoy"}
]

# Sample bearer token for demonstration
VALID_TOKEN = "Bearer mysecrettoken"

# Decorator for authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or auth_header != VALID_TOKEN:
            return {"error": "Authentication is required for this action, check your Authorization header"}, 401
        return f(*args, **kwargs)
    return decorated

@api.route('/books')
class BookList(Resource):
    def get(self):
        title_filter = request.args.get('title')
        author_filter = request.args.get('author')
        sort_by = request.args.get('sort', '').strip()

        filtered_books = books

        # Filter by title if provided
        if title_filter:
            filtered_books = [book for book in filtered_books if title_filter.lower() in book['title'].lower()]

        # Filter by author if provided
        if author_filter:
            filtered_books = [book for book in filtered_books if author_filter.lower() in book['author'].lower()]

        # Sort if sort_by is provided
        if sort_by:
            sort_keys = sort_by.split(',')
            for key in reversed(sort_keys):  # Reverse to apply primary sorting last
                reverse = key.startswith('-')
                field = key.lstrip('+-')
                if field in ['title', 'author']:
                    filtered_books = sorted(filtered_books, key=lambda x: x[field].lower(), reverse=reverse)

        return filtered_books

    @token_required
    def post(self):
        new_book = request.json
        if not new_book.get('title') or not new_book.get('author'):
            return {"error": "Missing required book fields (title, author)"}, 400

        # Assign a new unique ID to the new book
        new_id = max(book['id'] for book in books) + 1 if books else 1
        new_book['id'] = new_id

        # Add the new book to the in-memory list
        books.append(new_book)
        return new_book, 201


@api.route('/books/<int:book_id>')
class Book(Resource):
    def get(self, book_id):
        book = next((book for book in books if book['id'] == book_id), None)
        if not book:
            return {"error": "Book not found"}, 404
        return book

    @token_required
    def put(self, book_id):
        book = next((book for book in books if book['id'] == book_id), None)
        if not book:
            return {"error": "Book not found"}, 404

        updated_data = request.json
        book['title'] = updated_data.get('title', book['title'])
        book['author'] = updated_data.get('author', book['author'])
        return book

    @token_required
    def delete(self, book_id):
        global books
        books = [book for book in books if book['id'] != book_id]
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
