from bookModel import *
from flask_sqlalchemy import SQLAlchemy

db.create_all()
Book.add_book("Tulika ka copy", 99, 57687)
print(Book.get_all_books())
#db.session.commit()
#db.session.flush()
