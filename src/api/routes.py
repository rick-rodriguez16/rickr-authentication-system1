"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Invoice
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/token', methods=['POST'])
def generate_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Query the DB to check if user exists
    email = email.lower()
    user = User.query.filter_by(email=email, password=password).first()

    if user is None:
        response = {
            "msg": "User or Password does not match."
        }
        return jsonify(response), 401
    
    access_token = create_access_token(identity=user.id)
    response = {
        "access_token": access_token,
        "user_id": user.id,
        "msg": f"Welcome {user.email}! Please log in."
    }

    return jsonify(response), 200


@api.route('/signup', methods=['POST'])
def register_user():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Query to check if the email already exists
    email = email.lower()
    user = User.query.filter_by(email=email).first()

    if user is not None and user.email == email:
        response = {
            "msg": "User already exists."
        }
        return jsonify(response), 403
    
    new_user = User()
    new_user.email = email
    new_user.password = password
    new_user.is_active = True
    db.session.add(new_user)
    db.session.commit()

    response = {
        "msg": f"Awesome {new_user.email}! You successfully signed up!"
    }

    return jsonify(response), 200


@api.route('/invoice', methods=['GET'])
@jwt_required()
def get_invoices():
    # access the user_id of the current user with the access_token
    # you do that with get_jwt_identity
    user_id = get_jwt_identity()

    user = User.query.filter_by(id = user_id).first()

    # query and retrieve any and all invoices that are in the DB
    user_invoices = Invoice.query.filter_by(user_id=user_id).all()

    # we need to serialize the invoice objects and put them in an array
    # use a list comprehension (for loop) that will:
    # 1. Get each Invoice object and serialize() it
    # 2. Put them in the processed_invoices array
    processed_invoices = [each_invoice.serialize() for each_invoice in user_invoices]

    if user_invoices is None or len(user_invoices) == 0:
        response = {
            "msg": f"Hello {user.email}, you have no invoices.",
            'invoices': processed_invoices
        }   
        return jsonify(response), 200
    
    response = {
        'msg': f'Here are your invoices, {user.email}.',
        'invoices': processed_invoices
    }    
    return jsonify(response), 200


# work on the front end
# 1. create 3 new pages: /Signup, /Login, /Private
#     update layout.js as well
# 2. create the necessary inputs needed for signup.js and login.js
# 3. make sure that they are controlled inputs (useState)
# 4. include useContext and Context for flux applications
# 5. update flux.js to have token, message, invoices in the store
# 6. update and test actions to be able to retrieve a token and save it in localStorage