from .. import db, ma
from flask import jsonify

class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  event_name = db.Column(db.String(100), unique=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  players = db.Column(db.JSON)
  brackets = db.Column(db.JSON)

  def __init__(self, event_name, user_id, players, brackets):
    self.event_name = event_name
    self.user_id = user_id
    self.players = players
    self.brackets = brackets
    self.matches = []
