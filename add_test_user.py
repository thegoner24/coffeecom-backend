import os
from dotenv import load_dotenv
from app import create_app, db
from app.models.user import User
from flask import Flask

# Load environment variables
load_dotenv()

# Verify we're using PostgreSQL
db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
if 'postgresql' not in db_uri:
    print("ERROR: Not using PostgreSQL! Please check your .env file.")
    print(f"Current URI: {db_uri}")
    exit(1)

print(f"Using database: {db_uri}")

# Create the Flask app
app = create_app()

# Create a test user
with app.app_context():
    # Check if test user already exists
    test_user = User.query.filter_by(email='seller@test.com').first()
    
    if test_user:
        print(f"Test user already exists: {test_user.username} (ID: {test_user.id})")
    else:
        # Create a new seller user
        seller = User(
            username='testseller',
            email='seller@test.com',
            role='seller',
            first_name='Test',
            last_name='Seller'
        )
        seller.set_password('password123')
        
        # Create a new regular user
        user = User(
            username='testuser',
            email='user@test.com',
            role='user',
            first_name='Test',
            last_name='User'
        )
        user.set_password('password123')
        
        # Add to database
        db.session.add(seller)
        db.session.add(user)
        db.session.commit()
        
        print(f"Created test seller: {seller.username} (ID: {seller.id})")
        print(f"Created test user: {user.username} (ID: {user.id})")
    
    # List all users in the database
    users = User.query.all()
    print(f"\nTotal users in database: {len(users)}")
    print("ID | Username | Email | Role")
    print("-" * 50)
    for user in users:
        print(f"{user.id} | {user.username} | {user.email} | {user.role}")
