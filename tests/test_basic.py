import os
import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def client():
    """Create a test client for the app."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
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
    assert response.status_code == 200

def test_user_registration(client):
    """Test user registration endpoint."""
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'username': 'testuser',
        'role': 'user'
    })
    assert response.status_code == 201
    assert b'User registered successfully' in response.data
    
    # Verify user was created in database
    with client.application.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert user.username == 'testuser'
        assert user.role == 'user'
