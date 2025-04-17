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
    try:
        # Check if test users already exist
        seller_exists = User.query.filter_by(email='seller@test.com').first()
        user_exists = User.query.filter_by(email='user@test.com').first()
        
        if not seller_exists:
            # Create a new seller with shorter password hash
            seller = User(
                username='testseller',
                email='seller@test.com',
                role='seller',
                first_name='Test',
                last_name='Seller'
            )
            # Use a shorter password
            seller.set_password('test123')
            db.session.add(seller)
            print(f"Created test seller: {seller.username}")
        else:
            print(f"Test seller already exists: {seller_exists.username}")
            
        if not user_exists:
            # Create a new regular user
            user = User(
                username='testuser',
                email='user@test.com',
                role='user',
                first_name='Test',
                last_name='User'
            )
            # Use a shorter password
            user.set_password('test123')
            db.session.add(user)
            print(f"Created test user: {user.username}")
        else:
            print(f"Test user already exists: {user_exists.username}")
            
        # Commit changes
        db.session.commit()
        
        # List all users in the database
        users = User.query.all()
        print(f"\nTotal users in database: {len(users)}")
        print("ID | Username | Email | Role")
        print("-" * 50)
        for user in users:
            print(f"{user.id} | {user.username} | {user.email} | {user.role}")
            
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
