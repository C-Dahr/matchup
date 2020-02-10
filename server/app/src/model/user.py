from .. import db, ma
from .event import Event

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(100))
  email = db.Column(db.String(100), unique=True)
  challonge_username = db.Column(db.String(100), unique=True)
  api_key = db.Column(db.String(100))
  events = db.relationship('Event', backref='user', lazy=True)

  def __init__(self, username, password, email, challonge_username, api_key):
    self.username = username
    self.password = password
    self.email = email
    self.challonge_username = challonge_username
    self.api_key = api_key

class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'username', 'email', 'challonge_username', 'api_key')