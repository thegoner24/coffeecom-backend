import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URI from environment
db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
print(f"Database URI from .env: {db_uri}")

# Try to connect to PostgreSQL
try:
    # Parse the URI (assuming format: postgresql+psycopg2://user:pass@host:port/dbname)
    if db_uri and 'postgresql' in db_uri:
        parts = db_uri.replace('postgresql+psycopg2://', '').split('@')
        user_pass = parts[0].split(':')
        host_db = parts[1].split('/')
        
        user = user_pass[0]
        password = user_pass[1]
        host = host_db[0].split(':')[0]
        port = host_db[0].split(':')[1] if ':' in host_db[0] else '5432'
        dbname = host_db[1]
        
        print(f"Connecting to PostgreSQL: host={host}, port={port}, dbname={dbname}, user={user}")
        
        # Try to connect
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        print("Connection successful!")
        conn.close()
    else:
        print("Not a PostgreSQL URI or URI not found")
except Exception as e:
    print(f"Connection failed: {e}")
