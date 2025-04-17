import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Print current value
print(f"Current SQLALCHEMY_DATABASE_URI: {os.getenv('SQLALCHEMY_DATABASE_URI')}")

# Set the PostgreSQL URI directly
os.environ['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:gonetoer@localhost:5432/coffeecom_db'

# Print new value
print(f"New SQLALCHEMY_DATABASE_URI: {os.getenv('SQLALCHEMY_DATABASE_URI')}")

# Run Flask command if arguments provided
if len(sys.argv) > 1:
    from flask.cli import FlaskGroup
    from app import create_app
    
    cli = FlaskGroup(create_app=create_app)
    cli(sys.argv[1:])
