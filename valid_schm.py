from marshmallow import Schema, fields
from marshmallow.validate import Length, Range, OneOf


class CategorySchema(Schema):
    name = fields.String(validate=Length(min=3))


class LocationSchema(Schema):
    name = fields.String(validate=Length(min=3))


class UserSchema(Schema):
    # username = fields.String( required=True, validate=Length(min=3))
    username = fields.String(validate=Length(min=3))
    firstname = fields.String(validate=Length(min=3))
    lastname = fields.String(validate=Length(min=3))
    email = fields.String(validate=Length(min=5))
    password = fields.String(required=True, validate=Length(min=8))
    location_idlocation = fields.Integer(strict=True)


class AdSchema(Schema):

    text = fields.String(validate=Length(min=3))
    DataOfPublishing = fields.DateTime()
    status = fields.String(required=True, validate=OneOf("open, close"))
    idLocation = fields.Integer(strict=True)
    idCategory = fields.Integer(strict=True)
    idUser = fields.Integer(required=True)