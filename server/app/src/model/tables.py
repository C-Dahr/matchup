from enum import Enum
from .. import db, ma
from flask import jsonify

# helper tables file

class BracketPlayers(db.Model):
  player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True, nullable=False)
  bracket_id = db.Column(db.Integer, db.ForeignKey('bracket.id'), primary_key=True, nullable=False)
  name = db.Column(db.String(100), nullable=False)
  bracket = db.relationship('Bracket', back_populates='players')
  player = db.relationship('Player', back_populates='brackets')