"""
Comprehensive tests for the Flask application with coverage analysis
"""
import unittest
import json
from app import app, badFunction

class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_world(self):
        """Test main endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Hello from DevOps Lab!')
        self.assertIn('visits', data)
        
        # Test counter increment
        response2 = self.app.get('/')
        data2 = response2.get_json()
        self.assertGreater(data2['visits'], data['visits'])

    def test_health_check(self):
        """Test health endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'flask-app')

    def test_info_endpoint(self):
        """Test info endpoint"""
        response = self.app.get('/info')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('app_name', data)
        self.assertEqual(data['app_name'], 'DevOps Lab App')
        self.assertIn('python_version', data)
        self.assertIn('framework', data)

    def test_calculate_endpoint_default(self):
        """Test calculate endpoint with default values"""
        response = self.app.get('/calculate')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('result', data)

    def test_calculate_endpoint_custom_values(self):
        """Test calculate endpoint with custom values"""
        response = self.app.get('/calculate?x=15&y=20')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('result', data)
        # This should hit the x > 10 and y > 10 branch
        self.assertEqual(data['result'], 300)  # 15 * 20

    def test_calculate_endpoint_edge_cases(self):
        """Test calculate endpoint edge cases for better coverage"""
        # Test x > 10, y <= 10
        response = self.app.get('/calculate?x=15&y=5')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['result'], 20)  # 15 + 5
        
        # Test x <= 10
        response = self.app.get('/calculate?x=5&y=20')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['result'], 0)

    def test_bad_function_directly(self):
        """Test the badFunction directly for complete coverage"""
        # Test all branches of badFunction
        self.assertEqual(badFunction(15, 20), 300)  # x > 10, y > 10
        self.assertEqual(badFunction(15, 5), 20)    # x > 10, y <= 10
        self.assertEqual(badFunction(5, 20), 0)     # x <= 10

    def test_metrics_exposure(self):
        # NOT TESTED #
        response = self.app.get('/metrics')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()