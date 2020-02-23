from .. import db, ma
from flask import jsonify

class Event(db.Model):
  event_name = db.Column(db.String(100), primary_key=True, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
  players = db.Column(db.JSON)
  brackets = db.Column(db.JSON)

  def __init__(self, event_name, user_id, brackets, players):
    self.event_name = event_name
    self.user_id = user_id
    self.brackets = brackets
    self.players = players
    self.matches = []

class EventSchema(ma.Schema):
  class Meta:
    fields = ('event_name', 'user_id', 'players', 'brackets', 'matches')
