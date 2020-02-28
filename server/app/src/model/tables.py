from enum import Enum
from .. import db, ma
from flask import jsonify

# helper tables file

bracket_players = db.Table('bracket_players',
  db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True, nullable=False),
  db.Column('bracket_id', db.Integer, db.ForeignKey('bracket.id'), primary_key=True, nullable=False)
)

player_names = db.Table('player_names',
  player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True, nullable=False)
  bracket_id = db.Column(db.Integer, db.ForeignKey('bracket.id'), primary_key=True, nullable=False)
  name = db.Column(db.String(100), nullable=False)
)

player_challonge_ids = db.Table('player_challonge_ids'
  player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True, nullable=False)
  challonge_id = db.Column(db.Integer, primary_key=True, nullable=False)
)