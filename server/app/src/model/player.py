from .. import db, ma
from flask import jsonify
from .tables import Bracket_Players

class Player(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  brackets = db.relationship('Bracket_Players', back_populates='player')

