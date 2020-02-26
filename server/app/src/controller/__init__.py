import jwt
from ..model.user import User
from ..model.user import Event
from app.src.config import key
from itertools import cycle
import base64

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

def get_event_from_name(request, api):
  # check header for auth token
  if 'x-access-token' in request.headers:
    token = request.headers['x-access-token']
  else:
    api.abort(401, 'No user signed in.')
  # query database for event
  current_event = Event.query.filter_by(event_name=request.json['event_name']).first()
  if not current_event:
    api.abort(404, 'Event does not exist')
  return current_event

# xor encrypt/decrypt
def xor_crypt_string(data, encode = False, decode = False):
  if decode: 
    data = base64.decodestring(data.encode('utf-8'))
    data = data.decode('utf-8')
  xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
   
  if encode:
    x = base64.encodestring(xored.encode('utf-8')).strip()
    return x.decode('utf-8')
  return xored