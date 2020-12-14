from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Client(db.Model):
    __tablename__ = 'clients'
    id_client=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(60))
    address=db.Column(db.String(60))

class Product(db.Model):
    __tablename__ = 'products'
    id_product=db.Column(db.Integer, primary_key=True)
    description=db.Column(db.String(60))
    price=db.Column(db.String(45))


class Order(db.Model):
    __tablename__ = 'orders'
    id_order=db.Column(db.Integer, primary_key=True)
    id_client=db.Column(db.Integer, ForeignKey('clients.id_client'))
    date=db.Column(db.DateTime)
    address=db.Column(db.String(60))
    current_status=db.Column(db.Integer)

    order_lines = relationship('OrderLine')
    client = relationship('Client')

class OrderLine(db.Model):
    __tablename__ = 'order_lines'
    id_order=db.Column(db.Integer, ForeignKey('orders.id_order'), primary_key=True)
    id_product=db.Column(db.Integer, ForeignKey('products.id_product'), primary_key=True)
    quantity=db.Column(db.Integer)
    observations=db.Column(db.String(45))

    product = relationship('Product')

