"""
Contract Tests for User API
Demonstrates contract testing in cloud applications using Pact-like approach
"""
import unittest
import json
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.main import app


class TestUserAPIContract(unittest.TestCase):
    """Contract tests for the User API"""
    
    def setUp(self):
        """Set up test client"""
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_get_users_contract(self):
        """Test that GET /api/users returns expected contract"""
        response = self.client.get('/api/users')
        
        # Verify response structure
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
        # Verify response is a list
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_create_user_contract(self):
        """Test that POST /api/users follows expected contract"""
        user_data = {
            'username': 'contractuser',
            'email': 'contract@example.com'
        }
        
        response = self.client.post('/api/users', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        # Verify response structure
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')
        
        data = json.loads(response.data)
        
        # Verify required fields are present
        required_fields = ['id', 'username', 'email']
        for field in required_fields:
            self.assertIn(field, data)
        
        # Verify field types
        self.assertIsInstance(data['id'], int)
        self.assertIsInstance(data['username'], str)
        self.assertIsInstance(data['email'], str)
        
        # Verify field values
        self.assertEqual(data['username'], user_data['username'])
        self.assertEqual(data['email'], user_data['email'])
    
    def test_get_user_by_id_contract(self):
        """Test that GET /api/users/{id} follows expected contract"""
        # First create a user to test with
        user_data = {
            'username': 'contractuser',
            'email': 'contract@example.com'
        }
        
        create_response = self.client.post('/api/users', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Test the contract
        response = self.client.get(f'/api/users/{user_id}')
        
        # Verify response structure
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
        data = json.loads(response.data)
        
        # Verify required fields are present
        required_fields = ['id', 'username', 'email']
        for field in required_fields:
            self.assertIn(field, data)
        
        # Verify field types
        self.assertIsInstance(data['id'], int)
        self.assertIsInstance(data['username'], str)
        self.assertIsInstance(data['email'], str)
    
    def test_update_user_contract(self):
        """Test that PUT /api/users/{id} follows expected contract"""
        # First create a user to test with
        user_data = {
            'username': 'contractuser',
            'email': 'contract@example.com'
        }
        
        create_response = self.client.post('/api/users', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Test the update contract
        update_data = {
            'username': 'updatedcontractuser',
            'email': 'updatedcontract@example.com'
        }
        
        response = self.client.put(f'/api/users/{user_id}',
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        # Verify response structure
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
        data = json.loads(response.data)
        
        # Verify required fields are present
        required_fields = ['id', 'username', 'email']
        for field in required_fields:
            self.assertIn(field, data)
        
        # Verify field types
        self.assertIsInstance(data['id'], int)
        self.assertIsInstance(data['username'], str)
        self.assertIsInstance(data['email'], str)
        
        # Verify updated values
        self.assertEqual(data['username'], update_data['username'])
        self.assertEqual(data['email'], update_data['email'])
    
    def test_delete_user_contract(self):
        """Test that DELETE /api/users/{id} follows expected contract"""
        # First create a user to test with
        user_data = {
            'username': 'contractuser',
            'email': 'contract@example.com'
        }
        
        create_response = self.client.post('/api/users', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Test the delete contract
        response = self.client.delete(f'/api/users/{user_id}')
        
        # Verify response structure
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b'')
    
    def test_error_contract_user_not_found(self):
        """Test that 404 errors follow expected contract"""
        response = self.client.get('/api/users/999999')
        
        # Verify error response structure
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()

