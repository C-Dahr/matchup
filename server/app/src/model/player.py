from .. import db, ma
from flask import jsonify
from .tables import BracketPlayers

class Player(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
  brackets = db.relationship('BracketPlayers', back_populates='player')
  challonge_players = db.relationship('ChallongePlayer', back_populates='player')

class PlayerSchema(ma.Schema):
  class Meta:
    fields = ('id',)

