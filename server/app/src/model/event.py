from .. import db, ma

class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  event_name = db.Column(db.String(100), unique=True)
  list_of_players = db.Column(db.JSON) # not sure how to save a list of players
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # foreign key to user table
  brackets = db.Column(db.JSON) # list of ids (maybe use json?)


  def __init__(self, event_name, user_id, list_of_players, brackets):
    self.event_name = event_name
    self.user_id = user_id
    self.list_of_players = list_of_players
    self.brackets = brackets
