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

This project uses a Docker-based CI/CD pipeline with GitHub Actions and Koyeb.

### 1. Set up GitHub Secrets

Add the following secrets to your GitHub repository:

- `KOYEB_API_TOKEN`: Your Koyeb API token
- `SECRET_KEY`: A secure secret key for Flask
- `JWT_SECRET_KEY`: A secure secret key for JWT
- `SQLALCHEMY_DATABASE_URI`: Your PostgreSQL connection string
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

### 2. Create a Koyeb Account and Database

1. Sign up at [koyeb.com](https://koyeb.com)
2. Create a PostgreSQL database or use an external provider
3. Get your API token from Koyeb dashboard

### 3. How the CI/CD Pipeline Works

The workflow consists of three main jobs:

1. **Test**: Runs the test suite against a PostgreSQL database
2. **Build and Push**: Builds a Docker image and pushes it to GitHub Container Registry
3. **Deploy to Koyeb**: Deploys the Docker image to Koyeb using the Koyeb CLI

### 4. Deployment Process

When you push to the main branch, the CI/CD pipeline will automatically:

1. Run all tests to ensure code quality
2. Build a Docker image with your application
3. Push the image to GitHub Container Registry (ghcr.io)
4. Deploy the image to Koyeb using your configuration

You can monitor the deployment in the GitHub Actions tab of your repository and in the Koyeb dashboard.

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