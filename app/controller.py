from app import app, db
from models import *
from flask import render_template, jsonify
from flask import request, redirect, url_for
from datetime import datetime


@app.route('/')
def index():
    orders = Order.query.filter(Order.current_status == Order.CONFIRM_STATUS)
    return render_template('index.html', orders=orders)

@app.route('/editar-pedido/<int:id_order>/confirmar', methods=['GET', 'POST'])
def new_order_add_products_and_confirm(id_order):
    order = Order.query.get(id_order)
    if request.method == 'POST':
        add_item_to_order(order, request,confirm=True)
    return redirect(url_for('index'))

@app.route('/editar-pedido/<int:id_order>', methods=['GET', 'POST'])
def new_order_add_products(id_order):
    order = Order.query.get(id_order)
    if request.method == 'POST':
        add_item_to_order(order, request)
    order = Order.query.get(id_order)
    return render_template('add-order-items.html', order=order)


@app.route('/pedido/<int:id_order>/confirm',methods=['POST'])
def confirm_order(id_order):
    order = Order.query.get(id_order)
    order.current_status = Order.CONFIRM_STATUS
    db.session.merge(order)
    db.session.commit()
    return redirect(url_for('index'))



@app.route('/nuevo-pedido', methods=['GET', 'POST'])
def new_order():
    if request.method == 'POST':
        order= generate_new_order(request.form)
        return redirect(url_for('new_order_add_products', id_order=order.id_order))
    clients = Client.query.all()
    return render_template('new-order.html', clients=clients)

@app.route('/rest/clients')
def get_clients():
    clients = Client.query.all()
    return json.dumps(clients,cls=AlchemyEncoder)

@app.route('/rest/products')
def get_products():
    products = Product.query.all()
    return json.dumps(products,cls=AlchemyEncoder)

def add_item_to_order(order, request, confirm=False):
    id_product = request.form['id_product']
    quantity = int(request.form['quantity'])
    product = Product.query.get(id_product)
    order_line = OrderLine(id_product=id_product, quantity=quantity, unitary_price=product.price, total_price=int(product.price) * quantity)
    order.order_lines.append(order_line)
    if confirm:
        order.current_status = Order.CONFIRM_STATUS
    db.session.merge(order)
    db.session.commit()

def generate_new_order(form_data):

    if form_data.get('new_client', False) == 'on':
        address = form_data['address']
        telephone_number = form_data['telephone_number']
        name = form_data['name']
        client = Client(address=address,name=name, telephone_number=telephone_number)
        db.session.commit()
        id_client = client.id_client
    else:
        id_client = form_data['id_client']
    address = form_data['address']
    date = form_data['date']
    if form_data.get('is_delivery', False) == 'on':
        is_delivery = 1
    else:
        is_delivery = 0

    telephone_number = form_data['telephone_number']

    order = Order(id_client=id_client, address=address, date=date, is_delivery=is_delivery,telephone_number=telephone_number,current_status=Order.PENDING_CONFIRM_STATUS)
    db.session.add(order)
    db.session.commit()
    return order


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

