from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, fields, marshal_with, reqparse

app = Flask(__name__)
api = Api(app)
# Database
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# Init db
db = SQLAlchemy(app)


# User&UserList Class/Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    paid = db.Column(db.Boolean)
    dorm = db.Column(db.String(250))
    major = db.Column(db.String(250))

    def __init__(self, id, name, paid, dorm, major):
        self.id = id
        self.name = name
        self.paid = paid
        self.dorm = dorm
        self.major = major

resource_field = {
    'id': fields.Integer,
    'name': fields.String,
    'paid': fields.Boolean,
    'dorm': fields.String,
    'major': fields.String,
}

class UserList(Resource):
    @marshal_with(resource_field,  envelope='resource')
    def get(self, **kwargs):
        return Users.query.all()

class User(Resource):
    @marshal_with(resource_field,  envelope='resource')
    def get(self, user_id, **kwargs):
        return Users.query.get_or_404(user_id)

    @marshal_with(resource_field, envelope='resource')
    def delete(self, user_id, **kwargs):
        delete_user = Users.query.get_or_404(user_id)
        db.session.delete(delete_user)
        db.session.commit()
        return delete_user

    @marshal_with(resource_field,  envelope='resource')
    def post(self, user_id,  **kwargs):
        userinfo = request.get_json()
        if (userinfo['paid'] == "true"):
            paid = bool(1)
        else:
            paid = bool(0)
        new_user = Users(int(user_id), userinfo['name'], paid, userinfo['dorm'], userinfo['major'])
        db.session.add(new_user)
        db.session.commit()
        return Users.query.get(user_id)

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<string:user_id>')

if __name__ == '__main__':
    app.run()
