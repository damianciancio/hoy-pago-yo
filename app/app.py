from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SECRET_KEY'] = 'asddq132324{{´+'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://mywebuser:web000@localhost/hoy_pago_yo'

db=SQLAlchemy(app)

from controller import *

if __name__ == '__main__':
    app.run(debug=True)
