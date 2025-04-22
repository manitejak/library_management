from app.models import Book
from app import db
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError



def get_books(filters):
    """Retrieve books based on filtering criteria.
    
    Args:
        filters: Dictionary of filter parameters including:
            - title: Partial title match (case-insensitive)
            - author: Partial author match (case-insensitive)
            - category: Exact category match
            - book_summary: Partial summary match
            - is_available: Boolean availability filter
            
    Returns:
        List of Book objects matching the criteria
    """
    data = Book.query
    if 'title' in filters:
        data = data.filter(Book.title.ilike(f'%{filters["title"]}%'))
    
    if 'author' in filters:
        data = data.filter(Book.author.ilike(f"%{filters['author']}%"))
    
    if 'category' in filters:
            data = data.filter(Book.category == filters['category'])
        
    if 'book_summary' in filters:
        data = data.filter(Book.book_summary.ilike(f"%{filters['book_summary']}%"))
    
    if 'is_available' in filters:
        available = filters['is_available'].lower() in ('true','1','yes')
        data = data.filter(Book.is_available == available)

    return data.all()


def add_book(data):
    """Add one or multiple books to the library.
    
    Args:
        data: Either a single book dictionary or list of book dictionaries
        
    Returns:
        tuple: (response dictionary, HTTP status code)
            Success: Returns created book ID(s) with 201 status
            Error: Returns error message with appropriate status code
    """
    try:
        if isinstance(data,list):
            books = [Book(**book_data) for book_data in data]
            db.session.add_all(books)
            db.session.commit()
            return jsonify({
                'Message': f'added {len(books)} books',
                'book_ids':[book.id for book in books]
            }),201
        else:
            book = Book(**data)
            db.session.add(book)
            db.session.commit()
            return book
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'error':'Database error',
            'Message':str(e)
        }),400
    except Exception as e:
        return jsonify({
            'error':'Invalid data format',
            'Message': str(e)
        }),400


def update_book(book_id,data):
    """Update an existing book's information."""
    book = Book.query.get(book_id)
    if not book:
        return {'messgae': 'Book not found'},404
    for k,v in data.items():
        setattr(book,k,v)
    db.session.commit()
    return book

def delete_book(book_id):
    """Permanently remove a book from the library."""
    book =  Book.query.get(book_id)

    if not book:
        return {'Message':'Book not found'},404
    
    db.session.delete(book)
    db.session.commit()
    return '',204

