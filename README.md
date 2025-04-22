 Library Management System (LMS) – Flask REST API


Its a flask based application in scalable rest api for managing books,users and borrow history with user access limited to librarian and users based on resgitration and login based and librarian has books management previlage but users can search books details. It also has JWT based authentication for accessing all the apis based on login and providing the bearer token in authorization for enhanced security functionality

Features

User Management - Register and login with hashed passwords

JWT-based authentication - Role-based access for user, librarian

Book Management - Librarians can add, update, and delete books and  
    Track book availability, status (available, partial, borrowed) and Auto-handle book status and available copies

Borrowing System - Users can borrow/return books and 
    Dynamic due dates and borrowing history tracking and 
    Book inventory updated in real-time

Security - JWT for secure auth and 
    Password hashing via werkzeug.security and
    Role-based route protection

API Documentation:
    Interactive Swagger UI (Flask-RESTx)
    Try requests directly from browser
    Token-based authorization supported in Swagger

Tech Stack:
    Language:Python 3.9+
    Framework:Flask + Flask-RESTx
    Database:PostgreSQL (via SQLAlchemy ORM)
    Migrations:Flask-Migrate
    Auth:JWT (PyJWT) + Role decorators
    Docs:Swagger UI via Flask-RESTx


Setup Instructions:

1.Clone the repo
    git clone <https://github.com/manitejak/library_management.git>

    cd lms_backend

2.Create virtual environment
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate

    Install dependencies

    pip install -r requirements.txt

3.Configure PostgreSQL DB
    Edit config.py:

    SQLALCHEMY_DATABASE_URI = 'postgresql://<username>:<password>@localhost/library'

4.Run migrations

    flask db init
    flask db migrate -m "initial"
    flask db upgrade


5. flask run


6. Authentication

    Register via /auth/register

    Request:
    {
    "username": "new_user",
    "password": "securePassword123",
    "email_id": "user@example.com",
    "user_role": "user" 
    }
    
    Response (201 Created):

    {
    "message": "Registration Successful"
    }


    Login via /auth/login to get JWT token

    Request:
    {
    "username": "existing_user",
    "password": "securePassword123"
    }

    Response (200 OK):
    {
    "access_token": "eyJhbGciOi...",
    "user": {
        "id": 1,
        "username": "existing_user",
        "role": "user"
    }
    }


    Add the token in headers:

    Authorization: Bearer <your_token>

7.Sample Endpoints

    Authorization

    POST /auth/register

    POST /auth/login

8.Books

    GET /books/ – List/search books

    Query Params:
    title: Filter by title (partial match)
    author: Filter by author
    category: Filter by category
    is_available: Boolean filter

    Response (200 OK):
    [
    {
        "id": 1,
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "category": "technology",
        "is_available": true,
        "books_available": 3,
        "total_books": 5,
        "book_status": "partial_available",
        "book_summary": "Introduction to Python programming"
    }
    ]

    POST /books/ – Add book (librarian only)

    Request:
    {
    "title": "Clean Code",
    "author": "Robert Martin",
    "category": "technology",
    "total_books": 5,
    "book_summary": "Software craftsmanship guide"
    }

    Response (201 Created):
    {
    "ids": [2]
    }



    PUT /books/<id> – Update book

    DELETE /books/<id> – Delete book

9.Borrow

    POST /borrow/<book_id>/borrow – Borrow book

    Endpoint: POST /borrow/{book_id}/borrow

    Response (200 OK):
    {
    "message": "Book borrowed successfully!",
    "due_date": "15-07-2023",
    "books_available": 2,
    "book_status": "partial_available"
    }

    POST /borrow/<book_id>/return – Return book

    Endpoint: POST /borrow/{book_id}/return

    Response (200 OK):
    {
    "message": "Book returned successfully",
    "books_available": 3,
    "book_status": "available"
    }

    GET /borrow/history – View user's history
    Endpoint: GET /borrow/history

    Response (200 OK):
    [
    {
        "book_title": "Clean Code",
        "last_borrowed_date": "01-07-2023",
        "due_date": "11-07-2023",
        "returned_date": "05-07-2023",
        "status": "returned"
    }
    ]


10.Swagger UI

     http://localhost:5000/

11. in authorization with Bearer <your_token>

12.Design Choices

    Chose PostgreSQL for strong consistency, indexing, and relational integrity.

    Used JWT instead of API key system for better session management.

    Designed modular structure (views, models, urls, utils) for clean separation of concerns.

    Handled book availability and status at model level via custom logic.

