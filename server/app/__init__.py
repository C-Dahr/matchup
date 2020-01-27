from flask_restplus import Api
from flask import Blueprint

from .src.controller.user_controller import api as user_api
from .src.controller.auth_controller import api as auth_api

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Matchup REST API',
          version='1.0',
          description='REST API to be consumed by the Matchup front-end application'
          )

api.add_namespace(user_api, path='/user')
api.add_namespace(auth_api, path='/auth')