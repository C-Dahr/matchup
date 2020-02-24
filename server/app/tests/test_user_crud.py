from manage import app, db
import unittest
from flask_testing import TestCase
from flask import Flask
from app.src.config import basedir
from app.src.model.user import User
from werkzeug.security import generate_password_hash
import json
import base64

BASE_URL = 'http://localhost:5000/user'
LOGIN_URL = 'http://localhost:5000/auth'
invalid_id = 69 # nice

class BaseTestCase(TestCase):
  def create_app(self):
    app.config.from_object('app.src.config.TestingConfig')
    return app
  
  def setUp(self):
    password = generate_password_hash('password')
    test_user = User('testuser', password, 'test@gmail.com', 'testuser', 'challonge123')
    self.test_user = test_user

    db.drop_all()
    db.create_all()
    db.session.add(self.test_user)
    db.session.commit()

    valid_credentials = base64.b64encode(b'testuser:password').decode('utf-8')
    response = self.client.post(LOGIN_URL, headers={'Authorization': 'Basic ' + valid_credentials})
    returned = json.loads(response.data)
    tk_valid_user = returned['token']
    tk_invalid = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTV9.LZaaRkg7THSCD-8VDtjX43Wxn5gKktR6m8DJQDH2SpM'
    self.headers = {'Content-Type': 'application/json', 'x-access-token': tk_valid_user}
    self.badheaders = {'Content-Type': 'application/json', 'x-access-token': tk_invalid}

  def tearDown(self):
    db.session.remove()
    db.drop_all()


class TestCreateUser(BaseTestCase):
  def test_create_user(self):
    new_user = {
      'username': 'newuser',
      'password': 'pass345',
      'email': 'new@hotmail.com',
      'challonge_username': 'newuser',
      'api_key': 'AaBbCc987'
    }
    # send request
    response = self.client.post(BASE_URL, json=new_user, headers=self.headers)
    user_returned = json.loads(response.data)
    # get user from db
    user_from_db = User.query.get(user_returned['id'])
    self.assertEqual(new_user['username'], user_returned['username'], user_from_db.username)
    self.assertEqual(user_returned['id'], user_from_db.id)
  
  def test_create_user_missing_field(self):
    new_user = {
      'password': 'pass345',
      'email': 'new@hotmail.com',
      'challonge_username': 'newuser',
      'api_key': 'AaBbCc987'
    }
    response = self.client.post(BASE_URL, json=new_user, headers=self.headers)
    self.assert400(response)

  def test_create_user_username_already_exists(self):
    new_user = {
      'username': 'testuser',
      'password': 'pass345',
      'email': 'new@hotmail.com',
      'challonge_username': 'newuser',
      'api_key': 'AaBbCc987'
    }
    response = self.client.post(BASE_URL, json=new_user, headers=self.headers)
    self.assert_status(response, 409)


class TestDeleteUser(BaseTestCase):
  def test_delete_user(self):
    user_id = self.test_user.id
    response = self.client.delete(BASE_URL, headers=self.headers)
    user_returned = json.loads(response.data)
    # check correct user was removed
    self.assertEqual(user_id, user_returned['id'])
    # check that user was removed from database
    user_from_db = User.query.get(user_id)
    self.assertEqual(user_from_db, None)

  def test_delete_user_doesnt_exist(self):
    response = self.client.delete(BASE_URL, headers=self.badheaders)
    self.assert404(response)


class TestUpdateUser(BaseTestCase):
  def test_update_user(self):
    user_id = self.test_user.id
    new_info = {
      'username': 'testuser',
      'email': 'updated@email.ca',
      'challonge_username': 'testuser',
      'api_key': 'AaBbCc987'
    }
    response = self.client.put(BASE_URL, json=new_info, headers=self.headers)
    user_returned = json.loads(response.data)
    self.assertEqual(new_info['email'], user_returned['email'])
    # get the user in the database, confirm they are equal
    user_from_db = User.query.get(user_id)
    self.assertEqual(user_from_db, self.test_user)

  def test_update_user_doesnt_exist(self):
    new_info = {
      'username': 'testuser',
      'email': 'updated@email.ca',
      'challonge_username': 'testuser',
      'api_key': 'AaBbCc987'
    }
    response = self.client.put(BASE_URL, json=new_info, headers=self.badheaders)
    self.assert404(response)

  
  def test_update_user_username_already_exists(self):
    # add a new user
    new_user = {
      'username': 'newuser',
      'password': 'pass345',
      'email': 'new@hotmail.com',
      'challonge_username': 'newuser',
      'api_key': 'AaBbCc987'
    }
    response = self.client.post(BASE_URL, json=new_user, headers=self.headers)
    user_returned = json.loads(response.data)
    # try to update that user's username to "testuser"
    new_info = {
      'username': 'testuser',
      'email': 'new@hotmail.com',
      'challonge_username': 'newuser',
      'api_key': 'AaBbCc987'
    }
    response = self.client.put(BASE_URL, json=new_info, headers=self.headers)
    self.assert_status(response, 409)


class TestGetUsers(BaseTestCase):
  def test_get_user_by_id(self):
    response = self.client.get(BASE_URL, headers=self.headers)
    user_returned = json.loads(response.data)
    self.assertEqual(self.test_user.username, user_returned['username'])

  def test_get_user_by_invalid_id(self):
    user_id = invalid_id
    response = self.client.get(BASE_URL, headers=self.badheaders)
    self.assert404(response)

  def test_get_users(self):
    response = self.client.get(BASE_URL + '/all')
    users_returned = json.loads(response.data)
    self.assertTrue(len(users_returned) == 1)
    self.assertEqual(self.test_user.username, users_returned[0]['username'])

if __name__ == '__main__':
  unittest.main()