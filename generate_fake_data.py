from faker import Faker
from faker.providers.phone_number.es_ES import PhoneNumberProvider
from collections import defaultdict
from datetime import datetime
from models import Client, Order, OrderLine
import random
from app import db
from eralchemy import render_er
## Draw from SQLAlchemy base
render_er(db, 'erd_from_sqlalchemy.png')

pass

fake = Faker('es_ES')
fake.add_provider(PhoneNumberProvider)

clients = list()

for _ in range(1000):
    pass
    new_fake_client = Client()
    new_fake_client.name = fake.name()
    new_fake_client.address = fake.address()
    new_fake_client.id_city = random.randint(1,3)
    new_fake_client.telephone_number = fake.phone_number()
    new_fake_client.active = 1
    db.session.add(new_fake_client)



for _ in range(1000):
    pass
    new_fake_order = Order()
    new_fake_order.id_client = random.randint(1014,2010)
    new_fake_order.date = fake.date_between_dates(date_start=datetime(2021,1,1), date_end=datetime(2021,2,26)).isoformat()
    new_fake_order.address = fake.address()
    new_fake_order.current_status = Order.DELIVERED_STATUS
    new_fake_order.is_delivery = random.randint(0, 1) == 1
    new_fake_order.telephone_number = fake.phone_number()
    text = fake.text()
    new_fake_order.observations = (text[:255]) if len(text) > 255 else text

    new_order_line = OrderLine()
    new_order_line.id_product = 2
    new_order_line.quantity = 1
    new_order_line.unitary_price = 210
    new_order_line.total_price = 210

    new_fake_order.order_lines.append(new_order_line)
    db.session.add(new_fake_order)
db.session.commit()
