import os
import pytest
from app import create_app, db
from app.models.user import User

# Fix for Werkzeug compatibility issue
import werkzeug
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = '2.3.7'

@pytest.fixture
def client():
    """Create a test client for the app."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:'),
        'WTF_CSRF_ENABLED': False  # Disable CSRF for testing
    })
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_home_page(client):
    """Test that the home page loads."""
    response = client.get('/')
    assert response.status_code == 200 or response.status_code == 302  # 200 OK or 302 redirect

def test_user_registration(client):
    """Test user registration endpoint."""
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'username': 'testuser',
        'role': 'user'
    })
    assert response.status_code == 201
    assert b'User registered successfully' in response.data or b'registered' in response.data.lower()
    
    # Verify user was created in database
    with client.application.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert user.username == 'testuser'
        assert user.role == 'user'
