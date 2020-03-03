from .. import db, ma
from flask import jsonify
from .tables import BracketPlayers

class Player(db.Model):
<<<<<<< HEAD
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
=======
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
>>>>>>> b4661eb78146268c229c5c2b52cf79ba7618c083
  brackets = db.relationship('BracketPlayers', back_populates='player')
  challonge_players = db.relationship('ChallongePlayer', back_populates='player')

