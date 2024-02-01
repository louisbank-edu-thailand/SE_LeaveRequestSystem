import unittest
from flask_testing import TestCase
from se_leaverequestsystem.app import app, db, User

class TestLogin(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        # Create a test user
        test_user = User(user_name="testuser", password="testpassword")
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_successful_login(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.assert200(response)
        self.assertIn(b'Logged in successfully', response.data)

    def test_failed_login(self):
        response = self.client.post('/login', data=dict(
            username='nonexistentuser',
            password='wrongpassword'
        ), follow_redirects=True)
        self.assert200(response)
        self.assertIn(b'Invalid username or password', response.data)

if __name__ == '__main__':
    unittest.main()
