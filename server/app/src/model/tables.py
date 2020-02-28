from enum import Enum
from .. import db, ma
from flask import jsonify

# helper tables file
bracket_players = db.Table('bracket_players',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True, nullable=False),
    db.Column('bracket_id', db.Integer, db.ForeignKey('bracket.id'), primary_key=True, nullable=False)
)