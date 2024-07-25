from flask import request, jsonify
from models.schemas.customerSchema import customer_schema, customers_schema
from services import customerService #dont import the individual function, import the module as a whole
from marshmallow import ValidationError
from caching import cache
from utils.util import admin_required, token_required

def login():
    try:
        credentials = request.json
        token = customerService.login(credentials['username'], credentials['password'])
    except KeyError:
        return jsonify({'messages': 'Invalid payload, expecting username and password'}), 401
    
    if token:
        return jsonify(token), 200
    else:
        return jsonify({'messages': "Invalid username or password"}), 401


def save(): #name the controller the same as the service function

    try:
        #try to validate the incoming data, and deserialize
        customer_data = customer_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer_saved = customerService.save(customer_data)
    return customer_schema.jsonify(customer_data), 201


# @cache.cached(timeout=60)
@admin_required
def find_all():
    all_customers = customerService.find_all()
    return customers_schema.jsonify(all_customers), 200

@admin_required
def find_all_paginate():
    page = int(request.args.get("page"))
    per_page = int(request.args.get("per_page"))
    customers = customerService.find_all_paginate(page, per_page)
    return customers_schema.jsonify(customers), 200


def cart():
    pass
    #call customer cart service will return a user (based on an id either from route or token)
    #return customer to view useing CustomerCart Schema
    #i'll work on this later