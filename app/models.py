from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique = True, nullable = False,index=True)
    password = db.Column(db.String(250),nullable = False)
    email_id = db.Column(db.String(100),unique =  True, nullable = False,index=True)
    user_role = db.Column(db.String(20),nullable = False, default = 'user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime,default = datetime.utcnow, onupdate = datetime.utcnow)
    # created_by =  db.Column(db.String(36),db.ForeignKey('users.id'))
    # updated_by = db.Column(db.String(36),db.ForeignKey('users.id'))

    borrow_records = db.relationship('BookInventory', back_populates='user')


    def __intit__(self,**kwargs):
        kwargs.setdefault('user_role','user')
        kwargs.setdefault('is_active',True)
        kwargs.setdefault('created_at',datetime.utcnow())
        kwargs.setdefault('updated_at',datetime.utcnow())
        super().__init__(**kwargs)



class Book(db.Model):
    __tablename__= 'books'

    AVAILABLE_CATEGORIES = [
        'fiction',
        'non-fiction',
        'science',
        'history',
        'biography',
        'technology',
        'art',
        'children'
    ]
    DEFAULT_CATEGORY = 'technology'

    id =  db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250),unique = True,nullable = False,index=True)
    author = db.Column(db.String(100),nullable = False,index=True)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime,default = datetime.utcnow, onupdate = datetime.utcnow)
    total_books = db.Column(db.Integer,default=1)
    books_available = db.Column(db.Integer,default = 1)
    is_available = db.Column(db.Boolean, default=True)
    book_status = db.Column(db.String(30),default='available')
    category = db.Column(db.String(50),nullable = False, default =  DEFAULT_CATEGORY)
    book_summary = db.Column(db.String(500))

    borrow_records = db.relationship('BookInventory', back_populates='book')


    def __init__(self,**kwargs):
        total = kwargs.get('total_books',1)
        kwargs.setdefault('total_books',total)
        kwargs.setdefault('books_available',total)
        kwargs.setdefault('book_status','available')
        kwargs.setdefault('category',self.DEFAULT_CATEGORY)
        kwargs.setdefault('is_available',True)
        kwargs.setdefault('created_at',datetime.utcnow())
        kwargs.setdefault('updated_at',datetime.utcnow())
        super().__init__(**kwargs)



class BookInventory(db.Model):
    __tablename__ = 'book_inventory'

    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False,index=True)
    book_id= db.Column(db.Integer,db.ForeignKey('books.id'),nullable =  False,index=True)
    last_borrowed_date = db.Column(db.DateTime,default = datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    returned_date = db.Column(db.DateTime)
    book_status = db.Column(db.String(20), default = 'borrowed')

    book = db.relationship('Book', back_populates = 'borrow_records')
    user = db.relationship('User', back_populates = 'borrow_records')

    def __init__(self, **kwargs):
        kwargs.setdefault('last_borrowed_date',datetime.utcnow())
        kwargs.setdefault('book_status','borrowed')
        super().__init__(**kwargs)
    

    





    







