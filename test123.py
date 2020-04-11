from bookModel import *
from flask_sqlalchemy import SQLAlchemy
Book.add_book("Flask APIs", 99, 57687)
print(Book.get_all_books())
