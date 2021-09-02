from functools import wraps
from flask import Blueprint, json, jsonify, request
from flask_migrate import current
from car_inventory.helpers import token_required
from car_inventory.models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__,url_prefix = '/api')

@api.route('/getdata')
@token_required
def get_data(current_user_token):
    return { 'Something' : 'Here' }

# Create Car Endpoint
@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    color = request.json['color']
    year = request.json['year']
    max_speed = request.json['max_speed']
    miles_per_gallon = request.json['miles_per_gallon']
    price = request.json['price']
    user_token = current_user_token.token

    car = Car(make, model, color, year, max_speed, miles_per_gallon, price, user_token)
    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# Retrieve all cars endpoint
@api.route('/cars', methods=['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token=owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# Retrieve one car endpoint
@api.route('/cars/<id>', methods=['GET'])
@token_required
def get_car(current_user_token, id):
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)

# Update Car Endpoint
@api.route('/cars/<id>', methods=['POST','PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id) # Get Car Instance

    car.make = request.json['make']
    car.model = request.json['model']
    car.color = request.json['color']
    car.year = request.json['year']
    car.max_speed = request.json['max_speed']
    car.miles_per_gallon = request.json['miles_per_gallon']
    car.price = request.json['price']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Delete car Endpoint
@api.route('/cars/<id>', methods=['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)