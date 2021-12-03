from marshmallow import ValidationError
from flask import Blueprint, Response, request, jsonify
from databaseinf.inserts import session
from flask_bcrypt import Bcrypt
from valid_schm import UserSchema
from apischm.tablets import User
from flask_httpauth import HTTPBasicAuth
from apischm.user import auth

authentification = Blueprint('authentification', __name__)
bcrypt = Bcrypt()

s = session()



@authentification.route('/api/v1/authentication/register', methods=['POST'])
def register():
    data = request.get_json()

    try:
        UserSchema().load(data)
    except ValidationError as error:
        return jsonify(error.messages), 400

    exists = s.query(User.idUser).filter_by(username=data['username']).first()
    if exists:
        return Response(status=400, response='User with this username already exists.')

    hashed_password = bcrypt.generate_password_hash(data['password'])

    new_user = User(firstname=data['firstname'],
                    lastname=data['lastname'],
                    username=data['username'],
                    email=data['email'],
                    location_idlocation=data['location_idlocation'],
                    password=hashed_password)

    s.add(new_user)
    s.commit()

    return Response(status=200, response='Succesful operation')
