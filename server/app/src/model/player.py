from .. import db, ma
from flask import jsonify

class Player(db.Model):
  player_id = db.Column(db.Integer, primary_key=True, nullable=False)
  name = db.Column(db.String(100), nullable=False)
  seeds = db.Column(db.Integer, nullable=False)

  def __init__(self, id, name, seeds):
    self.player_id = id
    self.name = name
    self.seeds = seeds

  # compares the player_id passed in against all ids for this player
  def is_player(self, player_id):
    for bracket_id in self.bracket_ids:
      if player_id == bracket_id:
        return True
    return False

class PlayerSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'bracket_ids', 'seeds')
