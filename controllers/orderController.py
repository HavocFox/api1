from models.schemas.orderSchema import order_schema, orders_schema
from flask import request, jsonify
from marshmallow import ValidationError
from services import orderService

def save():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_order = orderService.save(order_data)
    return order_schema.jsonify(new_order), 201

def find_all():
    all_orders = orderService.find_all()
    return order_schema.jsonify(all_orders), 201

def find_all_paginate():
    page = int(request.args.get("page"))
    per_page = int(request.args.get("per_page"))
    orders = orderService.find_all_paginate(page, per_page)
    return orders_schema.jsonify(orders),200