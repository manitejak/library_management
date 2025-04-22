from app import db
from app.models import Book,BookInventory
from datetime import datetime,timedelta

def book_borrow(user,book_id):
    """Handle book borrowing process for a user.

    Args:
        user: The User instance borrowing the book
        book_id: ID of the book to borrow

    Returns:
        tuple: (response dictionary, HTTP status code)
            Success: Borrow confirmation with details (200)
            Failure: Error message with appropriate status code (400/404)
    """
    book = Book.query.get(book_id)
    print(book)
    if not book:
        return {'Message': 'No book found with this details'},404
    if book.books_available < 1:
        return {'Message': 'No copies of this book are available currently.Sorry'},400
    
    
    due_date = datetime.utcnow() + timedelta(days=10)
    borrow_update = BookInventory(
        user_id = user.id,
        book_id = book.id,
        last_borrowed_date = datetime.utcnow(),
        due_date = due_date,
        book_status = 'borrowed'
    )
    db.session.add(borrow_update)

    book.books_available-=1
    book.book_status = get_book_status(book)

    
    db.session.commit()

    return {
        'Message': 'Book borrowed successful!',
        'due_date': due_date.strftime("%d-%m-%Y"),
        'books_available': book.books_available,
        'book_status': book.book_status
    },200


def book_return(user,book_id):
    """Handle book return process for a user.

    Args:
        user: The User instance returning the book
        book_id: ID of the book being returned

    Returns:
        tuple: (response dictionary, HTTP status code)
            Success: Return confirmation with details (200)
            Failure: Error message with appropriate status code (404)
    """
    data = BookInventory.query.filter_by(user_id=user.id,book_id=book_id,
                                          book_status = 'borrowed').first()
    
    if not data:
        return{'Message':'No book borrowed at this time. Thank you'},404
    
    data.returned_date = datetime.utcnow()
    data.book_status = 'returned'

    book = Book.query.get(book_id)
    book.books_available += 1
    book.book_status = get_book_status(book)

    db.session.commit()

    return {
        'Message':'Book returned successfully',
        'books_available': book.books_available,
        'book_status': book.book_status
    },200




def get_book_status(book):
    """Determine the current status of a book based on availability.

    Args:
        book: The Book instance to check

    Returns:
        str: Status string ('available', 'partial_available', or 'borrowed')
    """
    if book.books_available == 0:
        return 'borrowed'
    elif book.books_available < book.total_books:
        return 'partial_available'
    else:
        return 'available'


def get_borrow_history(user):
    """Retrieve the borrowing history for a user.

    Args:
        user: The User instance whose history to fetch

    Returns:
        tuple: (list of history items, HTTP status code 200)
    """
    borrow_history = BookInventory.query.filter_by(user_id=user.id).order_by(BookInventory.last_borrowed_date.desc()).all()
    
    borrow_data = [{
        'book_title': borrow.book.title,
        'last_borrowed_date': borrow.last_borrowed_date.strftime("%d-%m-%Y"),
        'due_date': borrow.due_date.strftime("%d-%m-%Y"),
        'returned_date': borrow.returned_date.strftime("%d-%m-%Y") if borrow.returned_date else None,
        'status': borrow.book_status
    } for borrow in borrow_history]

    return borrow_data,200

