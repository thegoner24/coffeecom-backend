# CoffeeCom API Documentation

## Overview

CoffeeCom is a comprehensive e-commerce platform for coffee products with role-based access control. This API allows sellers to manage products and users to browse and purchase coffee products.

**🌐 Live API URL**: [https://nosy-saba-enclosure-cd2f8430.koyeb.app](https://nosy-saba-enclosure-cd2f8430.koyeb.app)  
**🧪 API Testing**: [APIdog Collection](https://5x7k4qnq6a.apidog.io)

## Authentication

All protected endpoints require a JWT token obtained through the login process.

### Headers

For protected endpoints, include the following header:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

## Role-Based Permissions

The API implements strict role-based access control:

### Seller Role
- Can create, update, and delete products
- Can view orders for their products
- Cannot place orders or add products to cart

### User Role
- Can browse products
- Can add products to cart
- Can place and manage orders
- Cannot create, update, or delete products

## API Endpoints

### Authentication

#### Register a New User
```
POST /api/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "Password123!",
  "username": "coffeeuser",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user"  // "user" or "seller"
}
```

**Response (201):**
```json
{
  "msg": "User registered successfully",
  "role": "user"
}
```

#### Login
```
POST /api/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "Password123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "coffeeuser",
    "role": "user"
  }
}
```

#### Get User Profile
```
GET /api/auth/profile
```

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "coffeeuser",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user"
}
```

#### Update User Profile
```
PUT /api/auth/profile
```

**Request Body:**
```json
{
  "first_name": "Updated",
  "last_name": "Name",
  "address": "456 New St, City"
}
```

**Response (200):**
```json
{
  "msg": "Profile updated"
}
```

### Products

#### Get All Products
```
GET /api/products/
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Ethiopian Yirgacheffe",
    "description": "Bright, fruity notes with a clean, sweet finish",
    "price": 14.99,
    "category_id": 1,
    "image_url": "https://example.com/ethiopian.jpg",
    "is_available": true,
    "discount_percentage": 0,
    "weight": 250.0,
    "dimensions": "10x5x15cm"
  },
  // More products...
]
```

#### Get Product by ID
```
GET /api/products/{product_id}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "Ethiopian Yirgacheffe",
  "description": "Bright, fruity notes with a clean, sweet finish",
  "price": 14.99,
  "category_id": 1,
  "image_url": "https://example.com/ethiopian.jpg",
  "is_available": true,
  "discount_percentage": 0,
  "weight": 250.0,
  "dimensions": "10x5x15cm"
}
```

#### Create Product (Seller Only)
```
POST /api/products/
```

**Request Body:**
```json
{
  "name": "Colombian Supremo",
  "description": "Well-balanced with a mild, clean taste",
  "price": 13.99,
  "category_id": 1,
  "image_url": "https://example.com/colombian.jpg",
  "is_available": true,
  "discount_percentage": 0,
  "weight": 250.0,
  "dimensions": "10x5x15cm"
}
```

**Response (201):**
```json
{
  "msg": "Product created",
  "id": 4
}
```

#### Update Product (Seller Only)
```
PUT /api/products/{product_id}
```

**Request Body:**
```json
{
  "price": 12.99,
  "discount_percentage": 5.0
}
```

**Response (200):**
```json
{
  "msg": "Product updated"
}
```

#### Delete Product (Seller Only)
```
DELETE /api/products/{product_id}
```

**Response (200):**
```json
{
  "msg": "Product deleted"
}
```

### Cart

#### View Cart
```
GET /api/cart/
```

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "product_id": 2,
      "name": "Colombian Supremo",
      "price": 13.99,
      "quantity": 2,
      "item_total": 27.98,
      "image_url": "https://example.com/colombian.jpg"
    }
  ],
  "total": 27.98
}
```

#### Add to Cart (User Only)
```
POST /api/cart/add
```

**Request Body:**
```json
{
  "product_id": 1,
  "quantity": 2
}
```

**Response (201):**
```json
{
  "msg": "Product added to cart"
}
```

#### Update Cart Item
```
PUT /api/cart/update/{item_id}
```

**Request Body:**
```json
{
  "quantity": 3
}
```

**Response (200):**
```json
{
  "msg": "Cart updated"
}
```

#### Remove Item from Cart
```
DELETE /api/cart/remove/{item_id}
```

**Response (200):**
```json
{
  "msg": "Item removed from cart"
}
```

#### Clear Cart
```
DELETE /api/cart/clear
```

**Response (200):**
```json
{
  "msg": "Cart cleared"
}
```

### Orders

#### Get All Orders
```
GET /api/orders/
```

**Response (200):**
```json
[
  {
    "id": 1,
    "order_number": "20250418123456-1",
    "status": "pending",
    "total": 27.98,
    "created_at": "2025-04-18T12:34:56",
    "items": [
      {
        "id": 1,
        "product_id": 2,
        "name": "Colombian Supremo",
        "price": 13.99,
        "quantity": 2,
        "total": 27.98
      }
    ]
  }
]
```

#### Get Order Details
```
GET /api/orders/{order_id}
```

**Response (200):**
```json
{
  "id": 1,
  "order_number": "20250418123456-1",
  "status": "pending",
  "total": 27.98,
  "shipping_address": "123 Coffee St, City",
  "payment_method": "credit_card",
  "created_at": "2025-04-18T12:34:56",
  "items": [
    {
      "id": 1,
      "product_id": 2,
      "name": "Colombian Supremo",
      "price": 13.99,
      "quantity": 2,
      "total": 27.98
    }
  ]
}
```

#### Create Order (User Only)
```
POST /api/orders/
```

**Request Body:**
```json
{
  "shipping_address": "123 Coffee St, City",
  "payment_method": "credit_card"
}
```

**Response (201):**
```json
{
  "msg": "Order created successfully",
  "order_id": 1,
  "order_number": "20250418123456-1"
}
```

#### Cancel Order
```
PUT /api/orders/{order_id}/cancel
```

**Response (200):**
```json
{
  "msg": "Order cancelled successfully"
}
```

### Transactions

#### Get User Transactions
```
GET /api/transactions/
```

**Response (200):**
```json
[
  {
    "id": 1,
    "order_id": 1,
    "user_id": 1,
    "amount": 27.98,
    "status": "completed",
    "payment_method": "credit_card",
    "payment_id": "pay_123456",
    "created_at": "2025-04-18T12:34:56",
    "updated_at": "2025-04-18T12:34:56"
  }
]
```

#### Get Transaction Details
```
GET /api/transactions/{transaction_id}
```

**Response (200):**
```json
{
  "id": 1,
  "order_id": 1,
  "user_id": 1,
  "amount": 27.98,
  "status": "completed",
  "payment_method": "credit_card",
  "payment_id": "pay_123456",
  "created_at": "2025-04-18T12:34:56",
  "updated_at": "2025-04-18T12:34:56"
}
```

#### Create Transaction
```
POST /api/transactions/
```

**Request Body:**
```json
{
  "order_id": 1,
  "amount": 27.98,
  "payment_method": "credit_card",
  "payment_id": "pay_123456"
}
```

**Response (201):**
```json
{
  "msg": "Transaction created",
  "id": 1
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "msg": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "msg": "Missing or invalid token"
}
```

### 403 Forbidden
```json
{
  "msg": "Seller access required"
}
```

### 404 Not Found
```json
{
  "msg": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Testing with APIdog

The complete API can be tested using our [APIdog Collection](https://5x7k4qnq6a.apidog.io).

1. Import the collection in APIdog
2. Set up your environment variables:
   - `baseUrl`: `https://nosy-saba-enclosure-cd2f8430.koyeb.app` (or `http://localhost:5000` for local testing)
   - `accessToken`: Will be automatically populated after login

3. Follow the testing flow:
   - Register a user (or seller)
   - Login to get a token
   - Test the various endpoints based on the user's role
