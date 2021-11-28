from marshmallow import ValidationError
from flask import Blueprint, Response, request, jsonify
from databaseinf.inserts import session
from apischm.tablets import User
from valid_schm import UserSchema
from flask_bcrypt import Bcrypt

user = Blueprint('user', __name__)
bcrypt = Bcrypt()

s = session()


@user.route('/api/v1/user/<username>', methods=['GET'])
def get_user_by_name(username):
    db_user = s.query(User).filter_by(username=username).first()
    if not db_user:
        return Response(status=404, response='User not found')

    user_data = {'idUser': db_user.idUser, 'username': db_user.username, 'firstname': db_user.firstname,
                 'lastname': db_user.lastname, 'location_idlocation': db_user.location_idlocation, 'email':db_user.email, 'password':db_user.password}
    return jsonify({"user": user_data})


@user.route('/api/v1/user/<username>', methods=['PUT'])
def update_user(username):
    data = request.get_json()

    try:
        UserSchema().load(data)
    except ValidationError as error:
        return jsonify(error.messages), 400

    db_user = s.query(User).filter_by(username=username).first()
    if not db_user:
        return Response(status=404, response='User not found')



    if 'username' in data.keys():
        exists = s.query(User.username).filter_by(username=data['username']).first()
        if exists:
            return Response(status=400, response='User with this username already exists.')
        db_user.username = data['username']

        if 'firstname' in data.keys():
            db_user.firstname = data['firstname']
        if "lastname" in data.keys():
            db_user.lastname = data['lastname']
        if 'password' in data.keys():
            hashed_password = bcrypt.generate_password_hash(data['password'])
            db_user.password = hashed_password
        if 'location_idlocation' in data.keys():
            db_user.location_idlocation = data['location_idlocation']
        if 'email' in data.keys():
            db_user.email = data['email']

            # Save changes
        s.commit()

        user_data = {'idUser': db_user.idUser, 'username': db_user.username, 'firstname': db_user.firstname,
                     'lastname': db_user.lastname,'email':db_user.email,'location_idlocation':db_user.location_idlocation}
        return jsonify({"user": user_data})
