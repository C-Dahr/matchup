from .. import db, ma
from flask import jsonify
from ..model.bracket import Bracket

class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
  event_name = db.Column(db.String(100), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  user = db.relationship('User', back_populates='events')
  brackets = db.relationship('Bracket', back_populates='event')

  def __init__(self, event_name, user_id):
    self.event_name = event_name
    self.user_id = user_id

  def update_number_of_setups_in_brackets(self, brackets_from_request):
    for bracket in brackets_from_request:
      bracket_object = Bracket.query.filter_by(event_id=self.id, bracket_id=bracket['bracket_id']).first()
      bracket_object.number_of_setups = bracket['number_of_setups']
    db.session.commit()

class EventSchema(ma.Schema):
  class Meta:
    fields = ('id', 'event_name', 'user_id')
