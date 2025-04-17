# CoffeeCom Backend

A Flask-based ecommerce backend for a coffee shop with PostgreSQL database integration, JWT authentication, and role-based access control (user and seller roles).

## Features

- User and seller authentication with JWT
- Role-based access control
- PostgreSQL database integration
- RESTful API for products, orders, and transactions
- Docker support for easy deployment
- CI/CD pipeline with GitHub Actions
- Deployment to Koyeb

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user or seller
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/profile` - Get user profile

### Products
- `GET /api/products` - Get all products
- `GET /api/products/:id` - Get product details
- `POST /api/products` - Add a new product (seller only)
- `PUT /api/products/:id` - Update a product (seller only)
- `DELETE /api/products/:id` - Delete a product (seller only)

### Dashboard
- `GET /api/dashboard/user` - User dashboard
- `GET /api/dashboard/seller` - Seller dashboard
- `GET /api/dashboard/admin` - Admin dashboard

## Local Development

### With Docker

```bash
# Start the application and database
docker-compose up

# Run in background
docker-compose up -d

# Stop the application
docker-compose down
```

### Without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL database
# Update .env file with your database credentials

# Run migrations
python -m flask db upgrade

# Start the server
python run_postgres.py
```

## CI/CD Setup with GitHub Actions and Koyeb

### 1. Set up GitHub Secrets

Add the following secrets to your GitHub repository:

- `KOYEB_API_TOKEN`: Your Koyeb API token
- `SECRET_KEY`: A secure secret key for Flask
- `JWT_SECRET_KEY`: A secure secret key for JWT
- `SQLALCHEMY_DATABASE_URI`: Your PostgreSQL connection string

### 2. Create a Koyeb Account and Database

1. Sign up at [koyeb.com](https://koyeb.com)
2. Create a PostgreSQL database or use an external provider
3. Get your API token from Koyeb dashboard

### 3. Push to GitHub

The CI/CD pipeline will automatically:

1. Run tests
2. Build Docker image
3. Deploy to Koyeb

## Database Setup

To initialize the database with test data:

```bash
# Add test users (user and seller)
python add_test_user_fixed.py

# Add sample coffee products
python add_coffee_direct.py
```

## Testing

```bash
pip install pytest pytest-cov
pytest --cov=app tests/
```