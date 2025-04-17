import os
import psycopg2
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Get database URI
db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
print(f"Current database URI: {db_uri}")

# Function to check if PostgreSQL is properly configured
def check_postgres_connection():
    try:
        if 'postgresql' not in db_uri:
            print("ERROR: Not using PostgreSQL. Please update your .env file.")
            return False
            
        # Parse connection details from URI
        conn_string = db_uri.replace('postgresql+psycopg2://', '')
        user_pass, host_db = conn_string.split('@')
        username, password = user_pass.split(':')
        host_port, dbname = host_db.split('/')
        
        if ':' in host_port:
            host, port = host_port.split(':')
        else:
            host, port = host_port, '5432'
            
        # Connect to PostgreSQL
        print(f"Connecting to PostgreSQL: {host}:{port}/{dbname} as {username}")
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=username,
            password=password
        )
        
        # Check if users table exists and show users
        with conn.cursor() as cur:
            # Check if users table exists
            cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
            table_exists = cur.fetchone()[0]
            
            if table_exists:
                print("✅ Users table exists")
                
                # Count users
                cur.execute("SELECT COUNT(*) FROM users")
                user_count = cur.fetchone()[0]
                print(f"Total users in database: {user_count}")
                
                # Show users if any exist
                if user_count > 0:
                    cur.execute("SELECT id, username, email, role FROM users")
                    users = cur.fetchall()
                    print("\nUsers in database:")
                    print("ID | Username | Email | Role")
                    print("-" * 50)
                    for user in users:
                        print(f"{user[0]} | {user[1]} | {user[2]} | {user[3]}")
                else:
                    print("No users found in the database.")
            else:
                print("❌ Users table does not exist. Migrations may not have run correctly.")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection error: {e}")
        return False

# Run the check
if __name__ == "__main__":
    success = check_postgres_connection()
    if not success:
        print("\nTo fix PostgreSQL connection:")
        print("1. Ensure PostgreSQL is running")
        print("2. Check your .env file has the correct connection string:")
        print("   SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://username:password@localhost:5432/dbname")
        print("3. Run migrations with: python set_db.py db upgrade")
        sys.exit(1)
    else:
        print("\n✅ PostgreSQL connection successful!")
