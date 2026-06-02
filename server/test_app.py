# Basic unit tests

# Import what necessary to ensure functionality of app
import unittest
from config import app, db

# Create a class for unit testing
class TestApp(unittest.TestCase):

    # Create a function to test with the configured set up
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()
        self.client = app.test_client()

    # Create a function to test if db is cleared after each test
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Create a function test signup process
    def test_signup(self):
        response = self.client.post('/signup', json={
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
    
    # Create a function test loggin process
    def test_login(self):
        self.client.post('/signup', json={'username': 'testuser', 'password': 'password123'})
        self.client.delete('/logout')
        response = self.client.post('/login', json={'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)

    # Create a function test logout process
    def test_logout(self):
        self.client.post('/signup', json={'username': 'testuser', 'password': 'password123'})
        response = self.client.delete('/logout')
        self.assertEqual(response.status_code, 204)
    
    # Create a function verify session
    def test_check_session(self):
        self.client.post('/signup', json={'username': 'testuser', 'password': 'password123'})
        response = self.client.get('/check_session')
        self.assertEqual(response.status_code, 200)

    # Create a function test note creation
    def test_create_note(self):
        self.client.post('/signup', json={'username': 'testuser', 'password': 'password123'})
        response = self.client.post('/notes', json={'title': 'Test', 'content': 'Some content'})
        self.assertEqual(response.status_code, 201)
    
    # Create a function test note retreival
    def test_get_notes(self):
        self.client.post('/signup', json={'username': 'testuser', 'password': 'password123'})
        response = self.client.get('/notes')
        self.assertEqual(response.status_code, 200)

    # Create a function test for unauthorized access
    def test_unauthorized_access(self):
        response = self.client.get('/notes')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()