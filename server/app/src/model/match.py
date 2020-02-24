class Match:
  def __init__(self, id, player1_id, player2_id, round_in_bracket, bracket_id, game_name):
    self.id = id
    self.player1_id = player1_id
    self.player2_id = player2_id
    self.round_in_bracket = round_in_bracket
    self.bracket_id = bracket_id
    self.game_name = game_name
    self.priority = 0
