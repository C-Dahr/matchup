from manage import app, db
import unittest
from flask_testing import TestCase
from flask import Flask
from app.src.config import basedir
from app.src.model.user import User
import json

BASE_URL = 'http://localhost:5000/user'

class BaseTestCaseClass(TestCase):
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

  def tearDown(self):
    db.session.remove()
    db.drop_all()


class TestCreateUser(BaseTestCaseClass):
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
  
  def test_create_user_missing_field(self):
    new_user = {
      'password': 'pass345',
      'email': 'new@hotmail.com',
      'api_key': 'AaBbCc987'
    }
    response = self.client.post(BASE_URL, json=new_user)
    self.assert400(response)

  def test_create_user_username_already_exists(self):
    new_user = {
      'username': 'testuser',
      'password': 'pass345',
      'email': 'new@hotmail.com',
      'api_key': 'AaBbCc987'
    }
    response = self.client.post(BASE_URL, json=new_user)
    self.assert_status(response, 409)


class TestDeleteUser(BaseTestCaseClass):
  def test_delete_user(self):
    user_id = self.test_user.id
    response = self.client.delete(BASE_URL + '/' + str(user_id))
    user_returned = json.loads(response.data)
    # check correct user was removed
    self.assertEqual(user_id, user_returned['id'])
    # check that user was removed from database
    user_from_db = User.query.get(user_id)
    self.assertEqual(user_from_db, None)

  def test_delete_user_doesnt_exist(self):
    user_id = 69 # invalid id (nice)
    response = self.client.delete(BASE_URL + '/' + str(user_id))
    self.assert404(response)


class TestUpdateUser(BaseTestCaseClass):
  def test_update_user(self):
    user_id = self.test_user.id
    new_info = {
      'username': 'testuser',
      'password': 'pass345',
      'email': 'updated@email.ca',
      'api_key': 'AaBbCc987'
    }
    response = self.client.put(BASE_URL + '/' + str(user_id), json=new_info)
    user_returned = json.loads(response.data)
    self.assertEqual(new_info['email'], user_returned['email'])
    # get the user in the database, confirm they are equal
    user_from_db = User.query.get(user_id)
    self.assertEqual(user_from_db, self.test_user)

  def test_update_user_doesnt_exist(self):
    user_id = 69 # invalid id (nice)
    new_info = {
      'username': 'testuser',
      'password': 'pass345',
      'email': 'updated@email.ca',
      'api_key': 'AaBbCc987'
    }
    response = self.client.put(BASE_URL + '/' + str(user_id), json=new_info)
    self.assert404(response)

  
  def test_update_user_username_already_exists(self):
    # add a new user
    new_user = {
      'username': 'newuser',
      'password': 'pass345',
      'email': 'new@hotmail.com',
      'api_key': 'AaBbCc987'
    }
    response = self.client.post(BASE_URL, json=new_user)
    user_returned = json.loads(response.data)
    # try to update that user's username to "testuser"
    new_info = {
      'username': 'testuser',
      'password': 'pass345',
      'email': 'new@hotmail.com',
      'api_key': 'AaBbCc987'
    }
    response = self.client.put(BASE_URL + '/' + str(user_returned['id']), json=new_info)
    self.assert_status(response, 409)


class TestGetUsers(BaseTestCaseClass):
  def test_get_user_by_id(self):
    response = self.client.get(BASE_URL + '/' + str(self.test_user.id))
    user_returned = json.loads(response.data)
    self.assertEqual(self.test_user.username, user_returned['username'])

  def test_get_user_by_invalid_id(self):
    user_id = 69
    response = self.client.get(BASE_URL + '/'+ str(user_id))
    self.assert404(response)

  def test_get_users(self):
    response = self.client.get(BASE_URL)
    users_returned = json.loads(response.data)
    self.assertTrue(len(users_returned) == 1)
    self.assertEqual(self.test_user.username, users_returned[0]['username'])

if __name__ == '__main__':
  unittest.main()