from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# Init app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost/dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(100))
  email = db.Column(db.String(100), unique=True)
  api_key = db.Column(db.String(100))

  def __init__(self, username, password, email, api_key):
    self.username = username
    self.password = password
    self.email = email
    self.api_key = api_key


class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'username', 'email', 'api_key')

# init schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/user', methods=['POST'])
def create_user():
  username = request.json['username']
  password = request.json['password']
  email = request.json['email']
  api_key = request.json['api_key']

  new_user = User(username, password, email, api_key)
  db.session.add(new_user)
  db.session.commit()
  return user_schema.jsonify(new_user)

@app.route('/user', methods=['GET'])
def get_all_users():
  all_users = User.query.all()
  return users_schema.jsonify(all_users)

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
  user = User.query.get_or_404(id)
  return user_schema.jsonify(user)

@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
  user = User.query.get_or_404(id)
  user.username = request.json['username']
  user.password = request.json['password']
  user.email = request.json['email']
  user.api_key = request.json['api_key']

  db.session.commit()
  return user_schema.jsonify(user)

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
  user = User.query.get_or_404(id)
  db.session.delete(user)
  db.session.commit()
  return user_schema.jsonify(user)

# run server
if __name__ == '__main__':
  app.run(debug=True)