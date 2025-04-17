import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL
BASE_URL = 'http://localhost:5000/api'

# Sample coffee products
COFFEE_PRODUCTS = [
    {
        "name": "Ethiopian Yirgacheffe",
        "description": "Light roast with floral and citrus notes. This Ethiopian coffee is known for its bright acidity and complex flavor profile.",
        "price": 14.99,
        "category_id": 1,  # Will be created if needed
        "image_url": "https://images.unsplash.com/photo-1611854779393-1b2da9d400fe",
        "is_available": True,
        "discount_percentage": 0,
        "weight": 0.34,  # in kg (12 oz)
        "dimensions": "8x4x2 inches"
    },
    {
        "name": "Colombian Supremo",
        "description": "Medium roast with caramel sweetness and nutty undertones. A balanced, smooth coffee with mild acidity.",
        "price": 12.99,
        "category_id": 1,
        "image_url": "https://images.unsplash.com/photo-1559525839-8f275eef9d67",
        "is_available": True,
        "discount_percentage": 5.0,
        "weight": 0.45,  # in kg (1 lb)
        "dimensions": "9x5x3 inches"
    },
    {
        "name": "Sumatra Mandheling",
        "description": "Dark roast with earthy, spicy notes and low acidity. Full-bodied with a smooth, syrupy mouthfeel.",
        "price": 15.99,
        "category_id": 1,
        "image_url": "https://images.unsplash.com/photo-1587734361993-0490df9a9b8b",
        "is_available": True,
        "discount_percentage": 0,
        "weight": 0.34,
        "dimensions": "8x4x2 inches"
    }
]

def create_category():
    """Create a coffee category if it doesn't exist"""
    print("Creating coffee category...")
    
    # First, try to login as seller
    login_data = {
        "email": "seller@test.com",
        "password": "test123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"Failed to login: {response.text}")
        return None
    
    token = response.json().get('access_token')
    if not token:
        print("No token received")
        return None
    
    print("Successfully logged in as seller")
    
    # Create coffee category (this endpoint might not exist in your API)
    # You may need to modify this part based on your actual API
    category_data = {
        "name": "Coffee Beans",
        "description": "Premium coffee beans from around the world"
    }
    
    # For this example, we'll assume category_id 1 exists or just use it
    return token, 1

def add_products(token, category_id):
    """Add coffee products using the API"""
    if not token:
        print("No authentication token available")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Add each product
    for i, product in enumerate(COFFEE_PRODUCTS):
        # Update category_id
        product["category_id"] = category_id
        
        print(f"Adding product: {product['name']}...")
        response = requests.post(
            f"{BASE_URL}/products/", 
            headers=headers,
            json=product
        )
        
        if response.status_code == 201:
            print(f"✅ Successfully added product: {product['name']}")
            print(f"   Product ID: {response.json().get('id')}")
        else:
            print(f"❌ Failed to add product: {response.text}")

def main():
    """Main function to add coffee products"""
    print("=== Adding Coffee Products to CoffeeCom ===")
    
    # Create category and get token
    token, category_id = create_category()
    
    # Add products
    add_products(token, category_id)
    
    print("\nDone!")

if __name__ == "__main__":
    main()
