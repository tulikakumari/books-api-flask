from flask import Flask,jsonify

app = Flask(__name__)
 
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
    }
]


    
@app.route('/books')
def get_books():
    return {'books':books}

@app.route('/books',method=['POST'])
def add_books():
    return jsonify(request.get_json())

    
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

app.run(port=5000)