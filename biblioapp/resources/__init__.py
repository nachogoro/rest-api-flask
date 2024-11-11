from .book_list import BookList
from .book import Book
from .book_stream import BookStream

def register_routes(api_namespace):
    api_namespace.add_resource(BookList, '/books')
    api_namespace.add_resource(Book, '/books/<int:book_id>')
    api_namespace.add_resource(BookStream, '/books/stream')
