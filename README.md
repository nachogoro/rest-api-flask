# Flask REST API Project

This project is a simple REST API for managing a collection of books. It’s
built with Flask, Flask-RESTx, and SQLAlchemy, featuring modularized code and
incremental development.

## Project Setup

### Prerequisites
- Python 3.10+
- `pip` (Python package manager)
- `git` (to clone the repository and navigate commits)

### Installation

1. **Clone the repository and checkout the 2024 branch**:
   ```bash
   git clone https://github.com/nachogoro/rest-api-flask.git
   cd flask-rest-api
   git checkout 2024
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python run.py
   ```

5. The API will be available at `https://127.0.0.1:5000/api/v1/` in the final
   version (previous versions may not support HTTPS or will not have any API
versioning).

## Usage

### API Endpoints

| Endpoint                 | Method | Description                                             |
|--------------------------|--------|---------------------------------------------------------|
| `/api/v1/books`          | GET    | Retrieve a list of books, with optional filters and pagination. |
| `/api/v1/books`          | POST   | Add a new book. Requires authentication.                |
| `/api/v1/books/<book_id>`| GET    | Retrieve a specific book by ID.                         |
| `/api/v1/books/<book_id>`| PUT    | Update a specific book's information. Requires authentication. |
| `/api/v1/books/<book_id>`| DELETE | Delete a book by ID. Requires authentication.           |
| `/api/v1/books/stream`   | GET    | Stream new books in real-time as they are added.        |

### Authentication

Some endpoints (POST, PUT, DELETE) require a Bearer token in the
`Authorization` header. Use the sample token:

```
Authorization: Bearer mysecrettoken
```

## Exploring the Git History

This project was built incrementally, with each commit representing an
improvement or feature addition. To explore these changes and understand how
the project evolved, follow these steps:

1. **View the commit history**:
   ```bash
   git log --oneline
   ```

   This command will show a summary of all commits. Each line lists a commit
hash and message describing the change.

2. **Check out a specific commit**:
   ```bash
   git checkout <commit-hash>
   ```

   Replace `<commit-hash>` with the hash of the commit you want to explore.
This lets you see the project at a specific stage in its development.

3. **Compare changes between commits**:
   To compare a specific commit with the previous one, use:

   ```bash
   git difftool <commit-hash>^
   ```

   This command shows the differences introduced by `<commit-hash>`. You’ll
need a diff tool (such as `vimdiff`, `meld`, or `kdiff3`) configured in Git for
this command.

4. **Return to the latest commit**:
   Once you’re done exploring, you can return to the latest commit on the main branch:

   ```bash
   git checkout main
   ```

## Additional Information

- **Database**: This project uses SQLite for simplicity. A file named `books.db` is created in the project directory upon running the application. You can populate the database with the `populate_db.py` script.
- **Documentation**: The API is self-documented with Swagger, available at `https://127.0.0.1:5000/api/v1`.

Happy learning!

