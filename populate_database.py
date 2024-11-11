from biblioapp import app, db
from biblioapp.models import BookModel

def populate_books():
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

    for book in books:
        existing_book = BookModel.query.filter_by(title=book['title'], author=book['author']).first()
        if not existing_book:
            new_book = BookModel(title=book['title'], author=book['author'])
            db.session.add(new_book)

    db.session.commit()
    print("Database populated with sample books.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the database and tables exist
        populate_books()
