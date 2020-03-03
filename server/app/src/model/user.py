from .. import db, ma
from .event import Event

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
  username = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  challonge_username = db.Column(db.String(100), unique=True)
  api_key = db.Column(db.String(100))
  events = db.relationship('Event', back_populates='user')

  def __init__(self, username, password, email, challonge_username, api_key):
    self.username = username
    self.password = password
    self.email = email
    self.challonge_username = challonge_username
    self.api_key = api_key

class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'username', 'email', 'challonge_username', 'api_key')