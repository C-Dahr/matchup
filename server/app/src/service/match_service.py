import challonge

def get_highest_priority_matches(event, bracket):
  list_of_matches = challonge.matches.index(bracket['id'], state='open')
  number_of_setups = bracket['number_of_setups']
  import pdb; pdb.set_trace()
  return list_of_matches[:number_of_setups]

