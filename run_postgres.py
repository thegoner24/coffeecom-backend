import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Verify we're using PostgreSQL
db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
if 'postgresql' not in db_uri:
    print("WARNING: Not using PostgreSQL! Please check your .env file.")
    print(f"Current URI: {db_uri}")
    print("Recommended: postgresql+psycopg2://postgres:yourpassword@localhost:5432/coffeecom_db")
    exit(1)
else:
    print(f"Using database: {db_uri}")

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    print("Starting server with PostgreSQL database...")
    app.run(debug=True, host="0.0.0.0", port=5000)
