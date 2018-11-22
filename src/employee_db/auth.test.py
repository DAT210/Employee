import os
import unittest

from util import *
from app import app

class authTestCase(unittest.TestCase):

    ## Testing authentication functionality ##
    ## To run all the tests: python auth.test.py -v ##

    # login page loading
    def test_login_page_loads(self):
        tester = app.test_client(self)
        resp = tester.get('/', content_type='html/text')
        self.assertEqual(resp.status_code, 200)

    # logged in with correct credentials
    
    def test_correct_login(self):
        tester = app.test_client(self)
        resp = tester.post('/login', data=dict(username='admin', password='admin'), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    # logged in with incorrect credentials

    def test_incorrect_login(self):
        tester = app.test_client(self)
        resp = tester.post('/login', data=dict(username='admin', password='notadmin'), follow_redirects=True)
        self.assertEqual(resp.status_code, 401)

    # logged in employee group 1, admin
    def test_group1_admin(self):
        tester = app.test_client(self)
        resp = tester.post('/login', data=dict(username='hr_admin', password='pass'), follow_redirects=True)
        self.assertIn(b'Employee Database', resp.data)
        self.assertIn(b'USER AUTHORITY: 1', resp.data)


    # logged in employee group 1, not admin
    def test_group1_not_admin(self):
        tester = app.test_client(self)
        resp = tester.post('/login', data=dict(username='hr_user', password='pass'), follow_redirects=True)
        self.assertIn(b'Employee Database', resp.data)
        self.assertIn(b'USER AUTHORITY: 2', resp.data)


    # logged in employee group 2, admin

    def test_group2_admin(self):
        tester = app.test_client(self)
        resp = tester.post('/login', data=dict(username='menu_admin', password='pass'), follow_redirects=True)
        self.assertIn(b'food preparation', resp.data)
        self.assertIn(b'USER AUTHORITY: 1', resp.data)


    # logged in employee group 2, not admin
    def test_group2_not_admin(self):
        tester = app.test_client(self)
        resp = tester.post('/login', data=dict(username='food_prep_user', password='pass'), follow_redirects=True)
        self.assertIn(b'food preparation', resp.data)
        self.assertIn(b'USER AUTHORITY: 2', resp.data)

    # logged in employee group 3, not admin

    def test_group3_not_admin(self):
        tester = app.test_client(self)
        resp = tester.post('/login', data=dict(username='delivery_user', password='pass'), follow_redirects=True)
        self.assertIn(b'To be delivered', resp.data)
        self.assertIn(b'USER AUTHORITY: 2', resp.data)
    
    # logged in employee group 4, not admin
    def test_group4_not_admin(self):
        tester = app.test_client(self)
        resp = tester.post('/login', data=dict(username='serving_user', password='pass'), follow_redirects=True)
        self.assertIn(b'Nothing to see here', resp.data)
        self.assertIn(b'USER AUTHORITY: 2', resp.data)


    # logout response
    def test_logout_page_loads(self):
        tester = app.test_client(self)
        resp = tester.get('/logout', content_type='html/text', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    # attempts to reach enpoints without logging in
    def test_no_login_get_employees(self):
        tester = app.test_client(self)
        resp = tester.get('/employees', content_type='document/json')
        self.assertEqual(resp.status_code, 401)

    
    def test_no_login_get_users(self):
        tester = app.test_client(self)
        resp = tester.get('/users', content_type='document/json')
        self.assertEqual(resp.status_code, 401)

    
    def test_no_login_get_employee(self):
        tester = app.test_client(self)
        resp = tester.get('/employees/3', content_type='document/json')
        self.assertEqual(resp.status_code, 401)

    def test_no_login_get_user(self):
        tester = app.test_client(self)
        resp = tester.get('/users/3', content_type='document/json')
        self.assertEqual(resp.status_code, 401)

    def test_no_login_create_employee(self):
        tester = app.test_client(self)
        resp = tester.post('/employees', data=dict(name="New test employee", group=2))
        self.assertEqual(resp.status_code, 401)

    def test_no_login_create_user(self):
        tester = app.test_client(self)
        resp = tester.post('/users', data=dict(username="Test user", ID=7, auth=2))
        self.assertEqual(resp.status_code, 401)




if __name__ == '__main__':
    unittest.main()