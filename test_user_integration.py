"""
Integration Tests for User API
Demonstrates integration testing in cloud applications
"""
import unittest
import json
import sys
import os
import tempfile

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.main import app
from src.models.user import db, User


class TestUserAPI(unittest.TestCase):
    """Integration tests for the User API"""
    
    def setUp(self):
        """Set up test client and database"""
        # Create a temporary database for testing
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        with app.app_context():
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_get_empty_users(self):
        """Test getting users when database is empty"""
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])
    
    def test_create_user(self):
        """Test creating a new user"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        
        response = self.client.post('/api/users', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        
        response_data = json.loads(response.data)
        self.assertEqual(response_data['username'], 'testuser')
        self.assertEqual(response_data['email'], 'test@example.com')
        self.assertIsNotNone(response_data['id'])
    
    def test_get_user_by_id(self):
        """Test getting a specific user by ID"""
        # First create a user
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        
        create_response = self.client.post('/api/users', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Now get the user by ID
        response = self.client.get(f'/api/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.data)
        self.assertEqual(response_data['id'], user_id)
        self.assertEqual(response_data['username'], 'testuser')
    
    def test_update_user(self):
        """Test updating an existing user"""
        # First create a user
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        
        create_response = self.client.post('/api/users', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Update the user
        update_data = {
            'username': 'updateduser',
            'email': 'updated@example.com'
        }
        
        response = self.client.put(f'/api/users/{user_id}',
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.data)
        self.assertEqual(response_data['username'], 'updateduser')
        self.assertEqual(response_data['email'], 'updated@example.com')
    
    def test_delete_user(self):
        """Test deleting a user"""
        # First create a user
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        
        create_response = self.client.post('/api/users', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Delete the user
        response = self.client.delete(f'/api/users/{user_id}')
        self.assertEqual(response.status_code, 204)
        
        # Verify user is deleted
        get_response = self.client.get(f'/api/users/{user_id}')
        self.assertEqual(get_response.status_code, 404)
    
    def test_get_nonexistent_user(self):
        """Test getting a user that doesn't exist"""
        response = self.client.get('/api/users/999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()

