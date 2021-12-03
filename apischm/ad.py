from marshmallow import ValidationError
from flask import Blueprint, Response, request, jsonify
from sqlalchemy.orm import Session

from databaseinf.inserts import session
from flask_bcrypt import Bcrypt
from apischm.tablets import Advertisment, User, Location, Category
from valid_schm import AdSchema
import datetime
s = session()
from apischm.user import auth

advertisement = Blueprint('advertisement', __name__)
bcrypt = Bcrypt()




@advertisement.route('/api/v1/advertisement', methods=['POST'])
@auth.login_required()
def add_ad():
    data = request.get_json()

    try:
        AdSchema().load(data)
    except ValidationError as error:
        return jsonify(error.messages), 400

    u = s.query(User).filter_by(username=auth.current_user()).first()
    if u.idUser != request.json["idUser"]:
        return {"message": "No Accessn"}, 403

    print(auth.current_user())

    exists = s.query(User.idUser).filter_by(idUser=data['idUser']).first()
    if not exists:
        return Response(status=404, response='User with this id was not found')

    exists = s.query(Location.idLocation).filter_by(idLocation=data['idLocation']).first()
    if not exists:
        return Response(status=404, response='Location with this id was not found')

    exists = s.query(Category.idCategory).filter_by(idCategory=data['idCategory']).first()
    if not exists:
        return Response(status=404, response='Category with this id was not found')

    loc = s.query(User).filter_by(location_idlocation=data['idLocation'], idUser=data['idUser']).first()
    if not loc:
        return Response(status=400, response='Wrong Location input. Input location right')


    new_ad = Advertisment(
        text=data['text'],
        DataOfPublishing=data['DataOfPublishing'],
        status=data['status'],
        idLocation=data['idLocation'],
        idCategory=data['idCategory'],
        idUser=data['idUser']
    )

    s.add(new_ad)
    s.commit()

    return Response(response='Successful adding ad')

# @advertisement.route('/api/v1/advertisement/<userId>', methods=['GET'])
# @auth.login_required()
# def get_ad_id(userId):
#     advertisements = s.query(Advertisment)
#
#     db_ad = s.query(Advertisment).filter_by(idUser=userId).first()
#     if not db_ad:
#         return Response(status=404, response='user with this Id wasn not founr')
#
#     # u = s.query(User).filter_by(username=auth.current_user()).first()
#     # adds = s.query(Advertisment.idUser).filter_by(idAdvertisment=userId).first()
#     # if u.idUser != adds[0]:
#     #     return {"message": "No Access"}, 403
#
#     u = s.query(User).filter_by(username=auth.current_user()).first()
#     if u.idUser != userId:
#         return {"message": "No Access"}, 403
#
#     ad_datas = {
#         'id': db_ad.idAdvertisment,
#         'text': db_ad.text,
#         'DataOfPublishing': db_ad.DataOfPublishing,
#         'status': db_ad.status,
#         'idLocation': db_ad.idLocation,
#         'idCategory': db_ad.idCategory,
#         'idUser': db_ad.idUser
#
#     }
#     return jsonify({"advertisement": ad_datas})


@advertisement.route('/api/v1/advertisement/<adId>', methods=['GET'])
@auth.login_required()
def get_ad_id(adId):

    advertisements = s.query(Advertisment)

    db_ad = s.query(Advertisment).filter_by(idAdvertisment=adId).first()
    if not db_ad:
        return Response(status=404, response='a advertisement with this Id wasn not founr')

    u = s.query(User).filter_by(username=auth.current_user()).first()
    adds = s.query(Advertisment.idUser).filter_by(idAdvertisment=adId).first()
    if u.idUser != adds[0]:
        return {"message": "No Access"}, 403

    # u = s.query(User).filter_by(username=auth.current_user()).first()
    # if u.idUser != adid:
    #     return {"message": "No Access"}, 403

    ad_datas = {
        'id': db_ad.idAdvertisment,
        'text': db_ad.text,
        'DataOfPublishing': db_ad.DataOfPublishing,
        'status': db_ad.status,
        'idLocation': db_ad.idLocation,
        'idCategory': db_ad.idCategory,
        'idUser': db_ad.idUser

    }
    return jsonify({"advertisement": ad_datas})




@advertisement.route('/api/v1/advertisement/<adId>', methods=['PUT'])
@auth.login_required()
def update_ad(adId):
    data = request.get_json()

    try:
        AdSchema().load(data)
    except ValidationError as error:
        return jsonify(error.messages), 400


    u = s.query(User).filter_by(username=auth.current_user()).first()
    adds = s.query(Advertisment.idUser).filter_by(idAdvertisment=adId).first()
    if u.idUser != adds[0]:
        return {"message": "No Access"}, 403


    db_ad = s.query(Advertisment).filter_by(idAdvertisment=adId).first()
    if not db_ad:
        return Response(status=404, response='Advertisement was not found')

    exists = s.query(User.idUser).filter_by(idUser=data['idUser']).first()
    if not exists:
        return Response(status=404, response='User with this id was not found')

    exists = s.query(Location.idLocation).filter_by(idLocation=data['idLocation']).first()
    if not exists:
        return Response(status=404, response='Location with this id was not found')

    exists = s.query(Category.idCategory).filter_by(idCategory=data['idCategory']).first()
    if not exists:
        return Response(status=404, response='Category with this id was not found')

    loc = s.query(User).filter_by(location_idlocation=data['idLocation'], idUser=data['idUser']).first()
    if not loc:
        return Response(status=400, response='Wrong Location input. Input location right')

    if 'text' in data.keys():
        db_ad.text = data['text']
    if 'DataOfPublishing' in data.keys():
        db_ad.DataOfPublishing = data['DataOfPublishing']
    if 'status' in data.keys():
        db_ad.status = data['status']
    if 'idLocation' in data.keys():
        db_ad.idLocation = data['idLocation']
    if 'idCategory' in data.keys():
        db_ad.idCategory = data['idCategory']

    s.commit()

    return Response("Ad was succesfuly edited")

@advertisement.route('/api/v1/advertisement/<adId>', methods=['DELETE'])
@auth.login_required()
def delete_audience(adId):
    db_ad = s.query(Advertisment).filter_by(idAdvertisment=adId).first()



    u = s.query(User).filter_by(username=auth.current_user()).first()
    adds = s.query(Advertisment.idUser).filter_by(idAdvertisment=adId).first()
    if u.idUser != adds[0]:
        return {"message": "No Access"}, 403

    if not db_ad:
        return Response(status=404, response='An ad with provided ID not found.')

    s.delete(db_ad)
    s.commit()

    return Response(response='Ad was successfully deleted.')



@advertisement.route('/api/v1/advertisement/username/<username>', methods=['GET'])
def get_advertisements_by_username(username):

    user = s.query(User).filter_by(username=username).first()
    if not user:
        return Response(status=404, response='User with such username was not found.')

    advertisement = s.query(Advertisment).filter_by(idLocation=user.location_idlocation, status='close')

    advertisement2 = s.query(Advertisment).filter_by(status='open')

    output1 = []
    for i in advertisement:
        output1.append({
                        'id': i.idAdvertisment,
                        'text': i.text,
                        'DataOfPublishing': i.DataOfPublishing,
                        'status': i.status,
                        'idLocation': i.idLocation,
                        'idCategory': i.idCategory,
                        'idUser': i.idUser})


    output2 = []
    for i in advertisement2:
        output2.append({
            'id': i.idAdvertisment,
            'text': i.text,
            'DataOfPublishing': i.DataOfPublishing,
            'status': i.status,
            'idLocation': i.idLocation,
            'idCategory': i.idCategory,
            'idUser': i.idUser})
    return jsonify({'advertisements':[{'open':output2}, {'close':output1}]})





