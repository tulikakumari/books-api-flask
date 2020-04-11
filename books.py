from flask import Flask,jsonify,request,Response
import json
from settings import *
 
books=[
    {
        'name':'the book of bible',
        'price':7.99,
       'isbn':984345678
    },
    {

        'name':'the book of Ramayan',
        'price':6.99,
        'isbn':984342345
    },
     {

        'name':'A',
        'price':16.99,
        'isbn':9843423233
    }

]

DEFAULT_PAGE_LIMIT=3
    
@app.route('/books')
def get_books():
    return {'books':books}


def validbookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False


@app.route('/books',methods=['GET','POST'])
def add_books():
    request_data = request.get_json()
    if(validbookObject(request_data)):
        new_book={
            "name":request_data['name'],
            "price":request_data['price'],
            "isbn":request_data['isbn']
        }
        books.insert(0,new_book)
        response=Response("",201,mimetype='application/json')
        response.headers['Location']="/books/"+str(new_book['isbn'])
        return response
    else:
        invalidbookObject={
            "error":"Invalid book object passed in the string",
            "helpstring":"'name':'bookname','price':'bookprice','isbn':'isbn number'"
        }
        response=Response(json.dumps(invalidbookObject),status= 401,mimetype='appliactaion/json')
        return response

    #  return jsonify(request.get_json())
       
    

@app.route('/books/<int:isbn>')
def get_books_by_isbn(isbn):
    return_value={}
    for book in books:
        if book["isbn"]==isbn:
            return_value={
                'name':book['name'],
                'price':book['price']
            }
    return jsonify(return_value)

def valid_put_request_data(request_data):
    if("name" in request_data and "price" in request_data):
        return "True"
    else:
        return "False"

@app.route('/books/<int:isbn>',methods=['PUT'])
def replace_books(isbn):
    request_data = request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidbookObject={
            "error":"valid book request must be passed in the request",
            "helpString":"Data passed id similar to this{'name':tfgh,'price':7.88}"
        }
        response = Response(json.dumbs(invalidbookObject),status=400,mimetype='appliactaion/json')
        return response
    new_book={
        'name':request_data['name'],
        'price':request_data['price'],
        'isbn':isbn
    }
    i = 0;
    for book in books:
        currentisbn = ["isbn"]
        # print(currentisbn)
        if currentisbn == isbn:
            # print("foundbook")
            books[i] = new_book
        i+=1
    response = Response("",status=204)
    return response
@app.route('/books/<int:isbn>',methods=['PATCH'])
def update_books(isbn):
    request_data = request.get_json()
    update_book = {}
    if("name" in request_data ):
        update_book["name"]=request_data['name']
    if("price" in request_data ):
        update_book["price"]=request_data['price']
    for book in books:
        if book["isbn"]==isbn:
            book.update(update_book)
    response=Response("",status=204)
    response.headers['Location'] = "/books/"+ str(isbn)
    return response
# PATCH /books /984345678
# {
#     'name':'Harry Pottr and the chamber of Secrets'
@app.route('/books/<int:isbn>',methods=['DELETE'])
def delete_book(isbn):
    i=0
    for book in books:
        if book["isbn"]==isbn:
            books.pop(i)
            response=Response("",status=204)
            return response
        i+=1
        invalidbookObject={
            "error":"Book with the given isbn is not found so therefore unable to delete",
        }
    response=Response(json.dumps(invalidbookObject),status=400,mimetype='appliactaion/json')
    return response;
app.run(port=5000)