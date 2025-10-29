"""
Unit Tests for User Model
Demonstrates unit testing in cloud applications
"""
import unittest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.models.user import User


class TestUserModel(unittest.TestCase):
    """Unit tests for the User model"""
    
    def test_user_creation(self):
        """Test creating a user instance"""
        user = User(username='testuser', email='test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
    
    def test_user_repr(self):
        """Test user string representation"""
        user = User(username='testuser', email='test@example.com')
        self.assertEqual(repr(user), '<User testuser>')
    
    def test_user_to_dict(self):
        """Test user serialization to dictionary"""
        user = User(username='testuser', email='test@example.com')
        user.id = 1  # Simulate database ID
        
        expected_dict = {
            'id': 1,
            'username': 'testuser',
            'email': 'test@example.com'
        }
        
        self.assertEqual(user.to_dict(), expected_dict)
    
    def test_user_validation(self):
        """Test user data validation"""
        # Test valid user
        user = User(username='validuser', email='valid@example.com')
        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.email)
        
        # Test that username and email are strings
        self.assertIsInstance(user.username, str)
        self.assertIsInstance(user.email, str)


if __name__ == '__main__':
    unittest.main()

