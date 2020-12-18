from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)
app.config['SECRET_KEY'] = 'asddq132324{{´+'
on_heroku = False
if 'HEROKU_APP' in os.environ:
    on_heroku = True
file = open('./config.txt')
db_url = file.read()
file.close()

if on_heroku:
    db_url = 'mysql+mysqlconnector://damian73:System32@damian73.mysql.pythonanywhere-services.com/hoy_pago_yo'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

db=SQLAlchemy(app)

from controller import *

if __name__ == '__main__':
    app.run(debug=True)
