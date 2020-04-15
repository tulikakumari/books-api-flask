from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/tulika/Desktop/flasktest/database1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
