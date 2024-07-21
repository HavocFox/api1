from flask import request, jsonify
from models.schemas.orderSchema import order_schema, orders_schema
from services import orderService
from marshmallow import ValidationError
from caching import cache


def save(): #name the controller the same as the service function

    try:
        #try to validate the incoming data, and deserialize
        order_data = order_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    order_saved = orderService.save(order_data)
    return order_schema.jsonify(order_data), 201

@cache.cached(timeout=60)
def find_all():
    all_orders = orderService.find_all()
    return order_schema.jsonify(all_orders), 201