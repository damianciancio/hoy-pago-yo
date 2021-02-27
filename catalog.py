from app import db
from sqlalchemy import ForeignKey, func, cast, DATE
from sqlalchemy.dialects import mysql
from datetime import datetime
from models import *

def get_orders_report(date_from, date_to, mode):
    if mode == 'days':
        query = db.session.query(cast(Order.date, DATE), func.count(Order.id_order))
        query = query.filter(Order.date >= date_from).filter(Order.date <= date_to)
        query_result = query.group_by(cast(Order.date, DATE)).order_by(cast(Order.date, DATE)).all()
        return list(map(lambda result: (result[0].isoformat(), result[1]), query_result))

    if mode == 'months':
        query = db.session.query(func.year(Order.date), func.month(Order.date), func.count(Order.id_order))
        query = query.filter(Order.date >= date_from).filter(Order.date <= date_to)
        query_result = query.group_by(func.year(Order.date), func.month(Order.date)).order_by(func.year(Order.date), func.month(Order.date)).all()
        return list(map(lambda result: (datetime(result[0], result[1], 1).isoformat(), result[2]), query_result))

