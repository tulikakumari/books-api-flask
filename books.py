from flask import Flask,jsonify,request,Response
import json
from settings import *
from bookModel import *
import jwt, datetime
from userModel import User
from functools import wraps
  
# books=[
#     {
#         'name':'the book of bible',
#         'price':7.99,
#        'isbn':984345678
#     },
#     {

#         'name':'the book of Ramayan',
#         'price':6.99,
#         'isbn':984342345
#     },
#      {

#         'name':'A',
#         'price':16.99,
#         'isbn':9843423233
#     }

# ]
books = Book.get_all_books()
DEFAULT_PAGE_LIMIT=3

app.config['SECRET_KEY']='meow'

@app.route('/login',methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username,password)
    if match:
        expiration_date = datetime.datetime.utcnow()+ datetime.timedelta(seconds=3600)
        token = jwt.encode({'exp':expiration_date},app.config['SECRET_KEY'],algorithm='HS256')
        return token
    else:
        return Response('',401,mimetype='application/json')

@app.route('/books/page/<int:page_number>')
def get_paginated_books(page_number):
    print(type(request.args.get('limit')))
    LIMIT = request.args.get('limit',DEFAULT_PAGE_LIMIT,int)
    startIndex = page_number* LIMIT- LIMIT
    endIndex = page_number*LIMIT
    print(startIndex)
    print(endIndex)
    return jsonify({'books':books[startIndex:endIndex]})

def token_required(f):  
    @wraps(f)
    def wrraper(*args,**kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token,app.config['SECRET_KEY'])
            return f(*args,**kwargs)
        except:
            return jsonify({'error':'Need a valid token to view this page'}),401
    return wrraper

@app.route('/books')

def get_books():
    return jsonify({'books':Book.get_all_books()})


def validbookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False


@app.route('/books',methods=['GET','POST'])
@token_required
def add_books():
    request_data = request.get_json()
    if(validbookObject(request_data)):
        Book.add_book(request_data['name'],request_data['price'],request_data['isbn'])
        # new_book={
        #     "name":request_data['name'],
        #     "price":request_data['price'],
        #     "isbn":request_data['isbn']
        # }
        # books.insert(0,new_book)
        response=Response("",201,mimetype='application/json')
        response.headers['Location']="/books/"+str(request_data['isbn'])
        return response
    else:
        invalidbookObject={
            "error":"Invalid book object passed in the string",
            "helpstring":"'name':'bookname','price':'bookprice','isbn':'isbn number'"
        }
        response=Response(json.dumps(invalidbookObject),status= 401,mimetype='application/json')
        return response

    #  return jsonify(request.get_json())
       
    

@app.route('/books/<int:isbn>')
def get_books_by_isbn(isbn):
    return_value=Book.get_book(isbn)
    # for book in books:
    #     if book["isbn"]==isbn:
    #         return_value={
    #             'name':book['name'],
    #             'price':book['price']
    #         }
    return jsonify(return_value)

def valid_put_request_data(request_data):
    if("name" in request_data and "price" in request_data):
        return "True"
    else:
        return "False"

@app.route('/books/<int:isbn>',methods=['PUT'])
@token_required
def replace_books(isbn):
    request_data = request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidbookObject={
            "error":"valid book request must be passed in the request",
            "helpString":"Data passed id similar to this{'name':tfgh,'price':7.88}"
        }
        response = Response(json.dumbs(invalidbookObject),status=400,mimetype='application/json')
        return response
    # new_book={
    #     'name':request_data['name'],
    #     'price':request_data['price'],
    #     'isbn':isbn
    # }
    # i = 0
    # for book in books:
    #     currentisbn = ["isbn"]
    #     # print(currentisbn)
    #     if currentisbn == isbn:
    #         # print("foundbook")
    #         books[i] = new_book
    #     i+=1
    Book.replace_book(isbn,request_data['name'],request_data['price'])
    response = Response("",status=204)
    return response
@app.route('/books/<int:isbn>',methods=['PATCH'])
@token_required
def update_books(isbn):
    request_data = request.get_json()
    # update_book = {}
    if("name" in request_data ):
        Book.update_book_name(isbn,request_data['name'])
        # update_book["name"]=request_data['name']
    if("price" in request_data ):
         Book.update_book_price(isbn,request_data['price'])
    #     update_book["price"]=request_data['price']
    # for book in books:
    #     if book["isbn"]==isbn:
    #         book.update(update_book)
    response=Response("",status=204)
    response.headers['Location'] = "/books/"+ str(isbn)
    return response
# PATCH /books /984345678
# {
#     'name':'Harry Pottr and the chamber of Secrets'
@app.route('/books/<int:isbn>',methods=['DELETE'])
@token_required
def delete_book(isbn):
    deleted = Book.delete_book(isbn)
    print("deleted",deleted)
    if(deleted):
       response = Response("",status=204)
       print(response)
       return response
    invalidbookObject={
            "error":"Book with the given isbn is not found so therefore unable to delete",
        }
    response=Response(json.dumps(invalidbookObject),status=400,mimetype='application/json')
    return response
app.run(port=5000)