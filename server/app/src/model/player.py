from .. import db, ma
from flask import jsonify
from .tables import BracketPlayers

class Player(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  brackets = db.relationship('BracketPlayers', back_populates='player')

