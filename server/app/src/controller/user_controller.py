from .. import db, ma
from ..model.user import UserSchema
from ..model.user import User
from flask import request, jsonify
from flask_restplus import Resource, Namespace

api = Namespace('user', description='user related operations')

# init schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@api.route('')
class UserListController(Resource):
  @api.doc('list of users')
  def get(self):
    users = User.query.all()
    return users_schema.jsonify(users)
  
  @api.doc('add a new user')
  def post(self):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    api_key = request.json['api_key']

    new_user = User(username, password, email, api_key)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

user_not_found = 'User not found.'

@api.route('/<id>')
@api.param('id', 'The User identifier')
class UserController(Resource):
  @api.doc('get a user')
  def get(self, id):
    user = User.query.get(id)
    if not user:
      api.abort(404, user_not_found)
    return user_schema.jsonify(user)
    
  @api.doc('update a user')
  def put(self, id):
    user = User.query.get(id)
    if not user:
      api.abort(404, user_not_found)
    
    user.username = request.json['username']
    user.password = request.json['password']
    user.email = request.json['email']
    user.api_key = request.json['api_key']

    db.session.commit()
    return user_schema.jsonify(user)

  @api.doc('delete a user')
  def delete(self, id):
    user = User.query.get(id)
    if not user:
      api.abort(404, user_not_found)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)
