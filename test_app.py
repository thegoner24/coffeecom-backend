"""
Simple test script for CoffeeCom backend that doesn't require pytest.
This script tests basic functionality to ensure our production-ready changes work.
"""
import os
import sys
import json
from app import create_app, db
from app.models.user import User

# Fix for Werkzeug compatibility issue
import werkzeug
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = '2.3.7'

def run_tests():
    """Run basic tests for the application."""
    # Set up test environment
    print("Setting up test environment...")
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:'),
        'WTF_CSRF_ENABLED': False  # Disable CSRF for testing
    })
    
    # Track test results
    tests_run = 0
    tests_passed = 0
    
    with app.test_client() as client:
        with app.app_context():
            # Set up database
            db.create_all()
            
            # Test 1: Home page
            print("\nTest 1: Home page")
            tests_run += 1
            response = client.get('/')
            if response.status_code == 200 or response.status_code == 302:
                print("✅ Home page test passed!")
                tests_passed += 1
            else:
                print(f"❌ Home page test failed! Status code: {response.status_code}")
            
            # Test 2: Health check endpoint
            print("\nTest 2: Health check endpoint")
            tests_run += 1
            response = client.get('/api/monitoring/health')
            if response.status_code == 200:
                data = json.loads(response.data)
                if data.get('status') in ['ok', 'degraded']:
                    print("✅ Health check test passed!")
                    tests_passed += 1
                else:
                    print(f"❌ Health check test failed! Unexpected status: {data.get('status')}")
            else:
                print(f"❌ Health check test failed! Status code: {response.status_code}")
            
            # Test 3: User registration
            print("\nTest 3: User registration")
            tests_run += 1
            response = client.post('/api/auth/register', json={
                'email': 'test@example.com',
                'password': 'password123',
                'username': 'testuser',
                'role': 'user'
            })
            if response.status_code == 201:
                print("✅ User registration test passed!")
                tests_passed += 1
            else:
                print(f"❌ User registration test failed! Status code: {response.status_code}")
                print(f"Response: {response.data.decode('utf-8')}")
            
            # Test 4: Database connection
            print("\nTest 4: Database connection")
            tests_run += 1
            try:
                user = User.query.filter_by(email='test@example.com').first()
                if user is not None and user.username == 'testuser':
                    print("✅ Database connection test passed!")
                    tests_passed += 1
                else:
                    print("❌ Database connection test failed! User not found or incorrect.")
            except Exception as e:
                print(f"❌ Database connection test failed! Error: {str(e)}")
            
            # Clean up
            db.session.remove()
            db.drop_all()
    
    # Print summary
    print("\n" + "="*50)
    print(f"Tests completed: {tests_run} run, {tests_passed} passed, {tests_run - tests_passed} failed")
    print("="*50)
    
    return tests_passed == tests_run

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
