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

class ChallongePlayer(db.Model):
  player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True, nullable=False)
  challonge_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
  player = db.relationship('Player', back_populates='challonge_players')

  def __init__(self, player_id, challonge_id):
    self.player_id = player_id
    self.challonge_id = challonge_id
