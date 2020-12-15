from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import json

class Client(db.Model):
    __tablename__ = 'clients'
    id_client=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(60))
    address=db.Column(db.String(60))
    telephone_number = db.Column(db.String(45))


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
    is_delivery=db.Column(db.Boolean)
    telephone_number = db.Column(db.String(45))
    observations = db.Column(db.String(150))

    PENDING_CONFIRM_STATUS = 1
    CONFIRM_STATUS = 2
    DELIVERED_STATUS = 3
    CANCELED_STATUS = 4

    order_lines = relationship('OrderLine')
    client = relationship('Client')

    def get_lines_description(self):
        descriptions = []
        for line in self.order_lines:
            descriptions.append(line.get_description())
        return ", ".join(tuple(descriptions))
    def get_total_price(self):
        total = 0
        for line in self.order_lines:
            total += line.total_price

        return total

class OrderLine(db.Model):
    __tablename__ = 'order_lines'
    id_order=db.Column(db.Integer, ForeignKey('orders.id_order'), primary_key=True)
    id_product=db.Column(db.Integer, ForeignKey('products.id_product'), primary_key=True)
    quantity=db.Column(db.Integer)
    observations=db.Column(db.String(45))
    unitary_price=db.Column(db.Float)
    total_price=db.Column(db.Float)

    product = relationship('Product')

    def get_description(self):
        return "x" + str(self.quantity) + " " + self.product.description + "($ " + str(self.total_price) + ")"

from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
