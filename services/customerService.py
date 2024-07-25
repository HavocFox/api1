from database import db
from models.customer import Customer
from sqlalchemy import select
from utils.util import encode_token

def login(username, password):  #login with unique info
    query = select(Customer).where(Customer.username == username)
    customer = db.session.execute(query).scalar_one_or_none() #DO WE HAVE SOMEONE?

    if customer and customer.password == password: #if cust assoc. with user, validate pass
        auth_token = encode_token(customer.id, customer.role.role_name)

        response = {
            'status': "success",
            'message': "Logged in successfully.",
            'auth_token': auth_token
        }
        return response

def save(customer_data):
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], password=customer_data['password'], phone=customer_data['phone'], username=customer_data['username'])
    db.session.add(new_customer)
    db.session.commit()

    db.session.refresh(new_customer)
    return new_customer

def find_all():

    query = select(Customer)
    all_customers = db.session.execute(query).scalars().all()
    return all_customers

def find_all_paginate(page, per_page):
    customers = db.paginate(select(Customer),page=page, per_page=per_page)
    return customers