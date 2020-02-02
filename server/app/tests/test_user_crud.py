from manage import app, db
import unittest
from flask_testing import TestCase
from flask import Flask
from app.src.config import basedir
from app.src.model.user import User
import json

BASE_URL = 'http://localhost:5000/user'

class TestCreateUser(TestCase):
  def create_app(self):
    app.config.from_object('app.src.config.TestingConfig')
    return app
  
  def setUp(self):
    test_user = User('testuser', 'password', 'test@gmail.com', 'challonge123')
    self.test_user = test_user

    db.create_all()
    db.session.add(self.test_user)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_create_user(self):
    new_user = {
      'username': 'newuser',
      'password': 'pass345',
      'email': 'new@hotmail.com',
      'api_key': 'AaBbCc987'
    }
    # send request
    response = self.client.post(BASE_URL, json=new_user)
    user_returned = json.loads(response.data)
    # get user from db
    user_from_db = User.query.get(user_returned['id'])
    
    self.assertEqual(new_user['username'], user_returned['username'], user_from_db.username)
    self.assertEqual(user_returned['id'], user_from_db.id)

class TestDeleteUser(TestCase):
  def create_app(self):
    app.config.from_object('app.src.config.TestingConfig')
    return app
  
  def setUp(self):
    test_user = User('testuser', 'password', 'test@gmail.com', 'challonge123')
    self.test_user = test_user

    db.drop_all()
    db.create_all()
    db.session.add(self.test_user)
    db.session.commit()
  


  # def test_delete_user(self):
  #   # delete the test user from the database


  # def test_delete_user_doesnt_exist(self):
  #   # delete a user using an invalid id


  # def test_update_user(self):
  #   # update the testuser
  #   # get the user in the database, confirm they are equal

  # def test_update_user_doesnt_exist(self):
  #   # update user with an invalid id

  
  # def test_update_user_username_already_exists(self):
  #   # add a new user
  #   # try to update that user's username to "test_user"


  # def test_get_user_by_id(self):


  # def test_get_user_by_invalid_id(self):


  # def test_get_users(self):

if __name__ == '__main__':
  unittest.main()