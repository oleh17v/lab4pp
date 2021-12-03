from marshmallow import ValidationError
from flask import Flask, Blueprint, Response, request, jsonify
from sqlalchemy.orm import Session
from validators import email

# from apischm.mysql import MySQL
from databaseinf.inserts import session
from apischm.tablets import User
from valid_schm import UserSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_httpauth import HTTPBasicAuth

from flask_bcrypt import Bcrypt

user = Blueprint('user', __name__)
bcrypt = Bcrypt()
s = session()
auth = HTTPBasicAuth()
# from config.config import conf

# mysql = MySQL(
#     user="root",
#     password="My1566",
#     server="localhost",
#     db_name="lab63"
# )
def check_json(function):
    def wrapper(*args, **kwargs):
        table_model, request = args
        correct = list(filter(lambda key: key not in table_model.__table__.columns.keys()[1:], request.json.keys())) == []
        return function(*args, **kwargs) and correct
    return wrapper

@check_json
def check_user(user_model, request):
    valid = True
    if request.json.get("email"):
        valid = valid and email(request.json.get("email"))
    idLocation = request.json.get("idLocation", None)
    if idLocation:
        valid = valid and (idLocation in range(1, 11))
    return valid

# def update_user(username, **values):
#     try:
#         table_obj = User.__table__
#         id = mysql.query(table_obj.columns.id).filter(table_obj.columns.username == username).scalar()
#         if not id:
#             return 404, None
#         mysql.update(User, id, **values)
#         user = mysql.query(table_obj).filter(table_obj.columns.id == id).one_or_none()
#         user_response = dict(zip(table_obj.columns.keys(), user))
#         return 200, user_response
#     except SQLAlchemyError as e:
#         return 400, e

#
# def get_all_usernames():
#     table_obj = User.__table__
#     return [res[0] for res in mysql.query(table_obj.columns.username).all()]


@auth.verify_password
def verify_password(username, password):
    try:
        user = s.query(User).filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return username
    except:
        return None

@user.route('/api/v1/user/<username>', methods=['GET'])

def get_user_by_name(username):
    db_user = s.query(User).filter_by(username=username).first()
    if not db_user:
        return Response(status=404, response='User not found')

    user_data = {'idUser': db_user.idUser, 'username': db_user.username, 'firstname': db_user.firstname,
                 'lastname': db_user.lastname, 'location_idlocation': db_user.location_idlocation, 'email':db_user.email, 'password':db_user.password}
    return jsonify({"user": user_data})




# @user.route('/api/v1/user/change_username', methods=['PUT'])
# @auth.login_required()
# def change_user():
#     print(auth.username())
#     if auth.username() not in get_all_usernames():
#         return {"message": "User can not be found"}, 404
#     if not request.json or not check_user(User, request):
#         return {"message": "Incorrect body"}, 400
#     updated_columns = request.json
#     response = update_user(auth.username(), **updated_columns)
#     del response[1]["password"]
#     return jsonify(response[1]), response[0]




# @user.route('/user/<login>', methods=['PUT'])
# @auth.login_required
# def userHandling(login):
#         userInfo = None
#         try:
#             schema = schemas.ValidateUserFieldsSchema()
#             data = request.json
#             userInfo = schema.load(data)
#         except ValidationError as err:
#             return f'Validation error.\n{err}', 400
#         except Exception as err:
#             return f'Internal server error. {err}', 500
#
#         try:
#             print(login)
#             commands.UpdateUserInfo(login, userInfo)
#         except ValueError as err:
#             return f'{err}', 404
#         except IntegrityError as err:
#             return f'Already exists', 403
#         except Exception as err:
#             return f'Internal server error. {err}', 500
#         return f'Info changed successfully'



@user.route('/api/v1/user/<username>', methods=['PUT'])
@auth.login_required()
def update_user(username):
    data = request.get_json()

    try:
        UserSchema().load(data)
    except ValidationError as error:
        return jsonify(error.messages), 400

    db_user = s.query(User).filter_by(username=username).first()
    if not db_user:
        return Response(status=404, response='User not found')

    u = s.query(User).filter_by(username=auth.current_user()).first()
    adds = s.query(User.idUser).filter_by(username=username).first()
    if u.idUser != adds[0]:
        return {"message": "No Access"}, 403

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