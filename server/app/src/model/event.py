from .. import db, ma
from flask import jsonify

class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
  event_name = db.Column(db.String(100), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  user = db.relationship('User', back_populates='events')
  brackets = db.relationship('Bracket', back_populates='event')

  def __init__(self, event_name, user_id):
    self.event_name = event_name
    self.user_id = user_id

class EventSchema(ma.Schema):
  class Meta:
    fields = ('id', 'event_name', 'user_id')
