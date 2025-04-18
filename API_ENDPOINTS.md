# CoffeeCom API Endpoints

Base URL: `https://nosy-saba-enclosure-cd2f8430.koyeb.app`

## Authentication

| Endpoint | Method | Description | Authentication Required |
|----------|--------|-------------|------------------------|
| `/api/auth/register` | POST | Register a new user | No |
| `/api/auth/login` | POST | Login and get access token | No |
| `/api/auth/profile` | GET | Get user profile | Yes |
| `/api/auth/profile` | PUT | Update user profile | Yes |

## Products

| Endpoint | Method | Description | Authentication Required | Role |
|----------|--------|-------------|------------------------|------|
| `/api/products/` | GET | Get all products | No | Any |
| `/api/products/:id` | GET | Get product by ID | No | Any |
| `/api/products/` | POST | Create a new product | Yes | Seller |
| `/api/products/:id` | PUT | Update a product | Yes | Seller |
| `/api/products/:id` | DELETE | Delete a product | Yes | Seller |

## Cart

| Endpoint | Method | Description | Authentication Required | Role |
|----------|--------|-------------|------------------------|------|
| `/api/cart/` | GET | View cart | Yes | User |
| `/api/cart/add` | POST | Add item to cart | Yes | User |
| `/api/cart/update/:id` | PUT | Update cart item quantity | Yes | User |
| `/api/cart/remove/:id` | DELETE | Remove item from cart | Yes | User |
| `/api/cart/clear` | DELETE | Clear entire cart | Yes | User |

## Orders

| Endpoint | Method | Description | Authentication Required | Role |
|----------|--------|-------------|------------------------|------|
| `/api/orders/` | GET | Get all user orders | Yes | User |
| `/api/orders/:id` | GET | Get order details | Yes | User |
| `/api/orders/` | POST | Create a new order | Yes | User |
| `/api/orders/:id/cancel` | PUT | Cancel an order | Yes | User |

## Categories

| Endpoint | Method | Description | Authentication Required | Role |
|----------|--------|-------------|------------------------|------|
| `/api/categories/` | GET | Get all categories | No | Any |
| `/api/categories/:id` | GET | Get category by ID | No | Any |
| `/api/categories/` | POST | Create a new category | Yes | Seller |
| `/api/categories/:id` | PUT | Update a category | Yes | Seller |
| `/api/categories/:id` | DELETE | Delete a category | Yes | Seller |

## Request/Response Examples

### Authentication

#### Register

**Request:**
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user"
}
```

**Response:**
```
Status: 201 Created
Content-Type: application/json

{
  "msg": "User created successfully"
}
```

#### Login

**Request:**
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```
Status: 200 OK
Content-Type: application/json

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "role": "user"
  }
}
```

### Products

#### Get All Products

**Request:**
```
GET /api/products/
```

**Response:**
```
Status: 200 OK
Content-Type: application/json

[
  {
    "id": 1,
    "name": "Ethiopian Yirgacheffe",
    "description": "Bright, fruity notes with a clean, sweet finish",
    "price": 14.99,
    "category_id": 1,
    "image_url": "https://example.com/images/ethiopian.jpg",
    "is_available": true,
    "discount_percentage": 0,
    "weight": "12 oz",
    "dimensions": "6x4x2 inches"
  },
  {
    "id": 2,
    "name": "Colombian Supremo",
    "description": "Full-bodied with a rich, caramel sweetness",
    "price": 12.99,
    "category_id": 1,
    "image_url": "https://example.com/images/colombian.jpg",
    "is_available": true,
    "discount_percentage": 10,
    "weight": "16 oz",
    "dimensions": "7x5x3 inches"
  }
]
```

#### Create Product (Seller Only)

**Request:**
```
POST /api/products/
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "name": "Brazilian Santos",
  "description": "Nutty and chocolatey with a light acidity",
  "price": 11.99,
  "category_id": 1,
  "image_url": "https://example.com/images/brazilian.jpg",
  "is_available": true,
  "discount_percentage": 0,
  "weight": "16 oz",
  "dimensions": "7x5x3 inches"
}
```

**Response:**
```
Status: 201 Created
Content-Type: application/json

{
  "id": 3,
  "name": "Brazilian Santos",
  "description": "Nutty and chocolatey with a light acidity",
  "price": 11.99,
  "category_id": 1,
  "image_url": "https://example.com/images/brazilian.jpg",
  "is_available": true,
  "discount_percentage": 0,
  "weight": "16 oz",
  "dimensions": "7x5x3 inches"
}
```

### Cart

#### Add to Cart

**Request:**
```
POST /api/cart/add
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "product_id": 1,
  "quantity": 2
}
```

**Response:**
```
Status: 200 OK
Content-Type: application/json

{
  "msg": "Item added to cart"
}
```

#### View Cart

**Request:**
```
GET /api/cart/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```
Status: 200 OK
Content-Type: application/json

{
  "cart_items": [
    {
      "id": 1,
      "product_id": 1,
      "product_name": "Ethiopian Yirgacheffe",
      "quantity": 2,
      "price": 14.99,
      "subtotal": 29.98
    }
  ],
  "total": 29.98
}
```

### Orders

#### Create Order

**Request:**
```
POST /api/orders/
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "shipping_address": "123 Main St, Anytown, USA",
  "payment_method": "credit_card"
}
```

**Response:**
```
Status: 201 Created
Content-Type: application/json

{
  "id": 1,
  "order_date": "2025-04-18T08:30:00Z",
  "status": "pending",
  "total_amount": 29.98,
  "items": [
    {
      "product_id": 1,
      "product_name": "Ethiopian Yirgacheffe",
      "quantity": 2,
      "price": 14.99
    }
  ]
}
```

## Authentication

All protected endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Error Responses

The API returns standard HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

Error response format:

```json
{
  "msg": "Error message describing what went wrong"
}
```

## Role-Based Access Control

- **User Role**: Can browse products, add products to cart, and place orders
- **Seller Role**: Can create, update, and delete products

Some endpoints have role restrictions:
- Sellers cannot add products to cart or place orders
- Users cannot create, update, or delete products

## Testing

You can test the API using the [APIdog Collection](https://apidog.com/collections/1234567)

## Live Deployment

The API is deployed at: `https://nosy-saba-enclosure-cd2f8430.koyeb.app`
