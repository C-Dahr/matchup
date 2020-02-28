from .. import db, ma
from flask import jsonify
from .tables import bracket_players

class Player(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  brackets = db.relationship("Bracket", secondary=bracket_players, back_populates='players')

class PlayerSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'seeds')
