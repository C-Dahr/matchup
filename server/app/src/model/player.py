class Player:
  def __init__(self, name, bracket_ids, seeds):
    self.name = name
    self.bracket_ids = bracket_ids
    self.seeds = seeds

  # compares the player_id passed in against all ids for this player
  def is_player(self, player_id):
    for bracket_id in self.bracket_ids:
      if player_id == bracket_id:
        return True
    return False
