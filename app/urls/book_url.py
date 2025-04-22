from flask import Blueprint,request
from flask_restx import Namespace,Resource,fields
from app.views.book_view import *
from app.utils.role_access import *

book_ns = Namespace('books', description= 'Books based CRUD')
book_model = book_ns.model('Book', {
    'id': fields.Integer(readOnly=True),
    'title': fields.String(required=True),
    'author': fields.String(required=True),
    'category': fields.String(),
    'is_available': fields.Boolean(),
    'books_available': fields.Integer(),
    'total_books': fields.Integer(),
    'book_status': fields.String(),
    'book_summary': fields.String()
})


book_list_model = book_ns.model('BookList', {
    'books': fields.List(fields.Nested(book_model))
})



@book_ns.route('/')
class BookList(Resource):
    @book_ns.doc('Book_data')
    @book_ns.param('title',description='search by title with partial match')
    @book_ns.param('author',description='search by author with partial match')
    @book_ns.param('category',description='search by category')
    @book_ns.param('book_summary',description='search in summary with partial match')
    @book_ns.param('is_available',description='filter with availability True or False')
    @book_ns.marshal_list_with(book_model)
    def get(self):
        """get all books based on the arguments with multiple search filters"""
        return get_books(request.args)

    @book_ns.doc('create_book_or_books')
    @book_ns.expect([book_model])
    @book_ns.response(201,'Success')
    @book_ns.response(400,'Validation Error')
    # @ns.marshal_with(book_model,code=200)
    @login
    @librarian
    def post(self,user):
        try:
            """create new book with single dict data or list of dict data"""
            data =  book_ns.payload
            if isinstance(data,list):
                books = [Book(**items) for items in data]
                db.session.add_all(books)
                db.session.commit()
                return {'ids':[b.id for b in books]},201
            else:
                book = Book(**data)
                db.session.add(book)
                db.session.commit()
                return {'id': book.id},201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                'error':'Database error',
                'Message':str(e)
            },400
        except Exception as e:
            return{
                'error':'Invalid data format',
                'Message': str(e)
            },400



@book_ns.route('/<int:book_id>')
@book_ns.response(404,'No book found')
@book_ns.param('id')
class BookResource(Resource):
    @book_ns.doc('get_book')
    @book_ns.marshal_with(book_model)
    def get(self,book_id):
        """fetch book by id"""
        book = Book.query.get(book_id)
        if not book:
            book_ns.abort(404,'No book found')
        return book
    
    @book_ns.doc('update_book')
    @book_ns.expect(book_model)
    @book_ns.marshal_with(book_model)
    @login
    @librarian
    def put(self,user,book_id):
        """update book with id"""
        return update_book(book_id,request.json)

    @book_ns.doc('delete_book')
    @book_ns.response(204,'book deleted')
    @login
    @librarian
    def delete(self,user,book_id):
        """delete book with id"""
        return delete_book(book_id)


