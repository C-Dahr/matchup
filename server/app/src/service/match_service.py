import challonge

def get_highest_priority_matches(event, bracket):
  list_of_matches = challonge.matches.index(bracket.bracket_id, state='open')
  return list_of_matches[:bracket.number_of_setups]

