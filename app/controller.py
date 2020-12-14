from app import app, db
from models import *
from flask import render_template
from flask import request, redirect, url_for

@app.route('/')
def index():
    orders = Order.query.all()
    return render_template('index.html', orders=orders)


@app.route('/editar-pedido/<int:id_order>', methods=['GET', 'POST'])
def new_order_add_products(id_order):
    order = Order.query.get(id_order)
    if request.method == 'POST':
        id_product = request.form['id_product']
        quantity = int(request.form['quantity'])
        order_line = OrderLine(id_product=id_product, quantity=quantity)
        order.order_lines.append(order_line)
        db.session.merge(order)
        db.session.commit()
    order = Order.query.get(id_order)
    return render_template('add-order-items.html', order=order)


@app.route('/nuevo-pedido', methods=['GET', 'POST'])
def new_order():
    if request.method == 'POST':
        id_client = request.form['id_client']
        address = request.form['address']
        date = request.form['date']
        order = Order(id_client=id_client, address=address, date=date)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('new_order_add_products', id_order=order.id_order))
    return render_template('new-order.html')


