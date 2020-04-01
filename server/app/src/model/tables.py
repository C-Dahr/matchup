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

class BracketPlayersSchema(ma.Schema):
  class Meta:
    fields = ('player_id', 'bracket_id', 'name')

class ChallongePlayer(db.Model):
  challonge_id = db.Column(db.Integer, primary_key=True, nullable=False)
  bracket_id = db.Column(db.Integer, db.ForeignKey('bracket.bracket_id'), primary_key=True, nullable=False)
  player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
  player = db.relationship('Player', back_populates='challonge_players')

  def __init__(self, player_id, challonge_id, bracket_id):
    self.player_id = player_id
    self.challonge_id = challonge_id
    self.bracket_id = bracket_id
