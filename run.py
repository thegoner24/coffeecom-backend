import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Use debug mode only in development
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(
        debug=debug_mode,
        host="0.0.0.0",
        port=int(os.getenv('PORT', 5000))
    )