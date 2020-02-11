import jwt
from ..model.user import User
from app.src.config import key

# helper method(s)
def get_user_from_auth_header(request, api):
  # check header for auth token
  if 'x-access-token' in request.headers:
    token = request.headers['x-access-token']
  else:
    api.abort(401, 'No user signed in.')
  # decode token and get user
  try:
    data = jwt.decode(token, key)
    current_user = User.query.filter_by(id=data['id']).first()
  except jwt.DecodeError as e:
    api.abort(401, 'Invalid token.')
  if not current_user:
      api.abort(404, 'User does not exist.')
  return current_user