from .. import db, ma
from flask import jsonify

class Event(db.Model):
<<<<<<< HEAD
  event_name = db.Column(db.String(100), primary_key=True, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
=======
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
  event_name = db.Column(db.String(100), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  user = db.relationship('User', back_populates='events')
  brackets = db.relationship('Bracket', back_populates='event')
>>>>>>> b4661eb78146268c229c5c2b52cf79ba7618c083

  def __init__(self, event_name, user_id):
    self.event_name = event_name
    self.user_id = user_id

class EventSchema(ma.Schema):
  class Meta:
    fields = ('event_name', 'user_id')
