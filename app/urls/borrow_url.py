from flask_restx import Namespace,Resource
from flask import request
from app.views.borrow_views import *
from app.utils.role_access import login


borrow_ns = Namespace('Borrow', description= 'Book borrowing Inventory')



@borrow_ns.route('/<int:book_id>/borrow')
class BorrowBook(Resource):
    @borrow_ns.doc(security='Bearer Token')
    @login
    def post(self,book_id,user):
        return book_borrow(user,book_id)


@borrow_ns.route('/<int:book_id>/return')
class ReturnBook(Resource):
    @borrow_ns.doc(security='Bearer Token')
    @login
    def post(self,book_id,user):
        return book_return(user,book_id)


@borrow_ns.route('/history')
class BorrowHistory(Resource):
    @borrow_ns.doc(security='Bearer Token')
    @login
    def get(self,user):
        return get_borrow_history(user)
    