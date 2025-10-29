"""
Performance Tests for User API
Demonstrates performance testing in cloud applications
"""
import unittest
import json
import time
import sys
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.main import app
from src.models.user import db


class TestUserAPIPerformance(unittest.TestCase):
    """Performance tests for the User API"""
    
    def setUp(self):
        """Set up test client and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        with app.app_context():
            db.drop_all()
    
    def test_single_user_creation_performance(self):
        """Test performance of creating a single user"""
        user_data = {
            'username': 'perfuser',
            'email': 'perf@example.com'
        }
        
        start_time = time.time()
        response = self.client.post('/api/users', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        end_time = time.time()
        
        # Verify response
        self.assertEqual(response.status_code, 201)
        
        # Performance assertion - should complete within 100ms
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.assertLess(response_time, 100, f"User creation took {response_time:.2f}ms, expected < 100ms")
    
    def test_bulk_user_creation_performance(self):
        """Test performance of creating multiple users"""
        num_users = 50
        users_data = []
        
        for i in range(num_users):
            users_data.append({
                'username': f'perfuser{i}',
                'email': f'perf{i}@example.com'
            })
        
        start_time = time.time()
        
        for user_data in users_data:
            response = self.client.post('/api/users', 
                                      data=json.dumps(user_data),
                                      content_type='application/json')
            self.assertEqual(response.status_code, 201)
        
        end_time = time.time()
        
        # Performance assertion - should complete within 5 seconds
        total_time = end_time - start_time
        self.assertLess(total_time, 5.0, f"Bulk creation of {num_users} users took {total_time:.2f}s, expected < 5s")
        
        # Calculate average time per user
        avg_time_per_user = (total_time / num_users) * 1000  # Convert to milliseconds
        self.assertLess(avg_time_per_user, 100, f"Average time per user: {avg_time_per_user:.2f}ms, expected < 100ms")
    
    def test_concurrent_user_creation_performance(self):
        """Test performance of concurrent user creation"""
        num_concurrent_users = 10
        
        def create_user(user_id):
            """Helper function to create a user"""
            user_data = {
                'username': f'concurrentuser{user_id}',
                'email': f'concurrent{user_id}@example.com'
            }
            
            start_time = time.time()
            response = self.client.post('/api/users', 
                                      data=json.dumps(user_data),
                                      content_type='application/json')
            end_time = time.time()
            
            return {
                'status_code': response.status_code,
                'response_time': (end_time - start_time) * 1000,
                'user_id': user_id
            }
        
        start_time = time.time()
        
        # Use ThreadPoolExecutor for concurrent requests
        with ThreadPoolExecutor(max_workers=num_concurrent_users) as executor:
            futures = [executor.submit(create_user, i) for i in range(num_concurrent_users)]
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        
        # Verify all requests succeeded
        for result in results:
            self.assertEqual(result['status_code'], 201)
        
        # Performance assertions
        total_time = end_time - start_time
        self.assertLess(total_time, 2.0, f"Concurrent creation of {num_concurrent_users} users took {total_time:.2f}s, expected < 2s")
        
        # Check individual response times
        response_times = [result['response_time'] for result in results]
        max_response_time = max(response_times)
        avg_response_time = sum(response_times) / len(response_times)
        
        self.assertLess(max_response_time, 500, f"Max response time: {max_response_time:.2f}ms, expected < 500ms")
        self.assertLess(avg_response_time, 200, f"Average response time: {avg_response_time:.2f}ms, expected < 200ms")
    
    def test_get_users_performance_with_data(self):
        """Test performance of getting users when database has data"""
        # First, create some users
        num_users = 100
        for i in range(num_users):
            user_data = {
                'username': f'datauser{i}',
                'email': f'data{i}@example.com'
            }
            response = self.client.post('/api/users', 
                                      data=json.dumps(user_data),
                                      content_type='application/json')
            self.assertEqual(response.status_code, 201)
        
        # Now test the performance of getting all users
        start_time = time.time()
        response = self.client.get('/api/users')
        end_time = time.time()
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        users = json.loads(response.data)
        self.assertEqual(len(users), num_users)
        
        # Performance assertion - should complete within 200ms
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.assertLess(response_time, 200, f"Getting {num_users} users took {response_time:.2f}ms, expected < 200ms")
    
    def test_memory_usage_stability(self):
        """Test that repeated operations don't cause memory leaks"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Perform many operations
        for i in range(100):
            # Create user
            user_data = {
                'username': f'memuser{i}',
                'email': f'mem{i}@example.com'
            }
            create_response = self.client.post('/api/users', 
                                             data=json.dumps(user_data),
                                             content_type='application/json')
            self.assertEqual(create_response.status_code, 201)
            
            # Get user
            user = json.loads(create_response.data)
            get_response = self.client.get(f'/api/users/{user["id"]}')
            self.assertEqual(get_response.status_code, 200)
            
            # Delete user
            delete_response = self.client.delete(f'/api/users/{user["id"]}')
            self.assertEqual(delete_response.status_code, 204)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory should not increase by more than 50MB
        self.assertLess(memory_increase, 50, f"Memory increased by {memory_increase:.2f}MB, expected < 50MB")


if __name__ == '__main__':
    unittest.main()

