import requests
import json

# Base URL - change to your deployed URL if needed
BASE_URL = "http://localhost:5000"  # or "https://nosy-saba-enclosure-cd2f8430.koyeb.app"

def test_auth_flow():
    # 1. Register a new user with seller role
    import random
    random_suffix = random.randint(1000, 9999)
    email = f"test{random_suffix}@example.com"
    
    register_data = {
        "email": email,
        "password": "Password123!",
        "username": f"testuser{random_suffix}",
        "first_name": "Test",
        "last_name": "User",
        "role": "seller"  # Set role to seller for product creation
    }
    register_response = requests.post(
        f"{BASE_URL}/api/auth/register", 
        json=register_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Register Response: {register_response.status_code}")
    print(register_response.json())
    print("-" * 50)

    # 2. Login to get token
    login_data = {
        "email": email,  # Use the same email we just registered
        "password": "Password123!"
    }
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login", 
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Login Response: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print("Login failed!")
        print(login_response.text)
        return
    
    # Extract token
    token = login_response.json().get("access_token")
    print(f"Token: {token[:20]}...")  # Print first 20 chars for security
    print("-" * 50)
    
    # 3. Get profile with token
    profile_response = requests.get(
        f"{BASE_URL}/api/auth/profile",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    print(f"Profile Response: {profile_response.status_code}")
    print(json.dumps(profile_response.json(), indent=2) if profile_response.status_code == 200 else profile_response.text)
    print("-" * 50)
    
    # 4. Test products endpoint - GET (no auth required)
    products_response = requests.get(f"{BASE_URL}/api/products/")
    print(f"Products Response: {products_response.status_code}")
    if products_response.status_code == 200:
        products = products_response.json()
        print(f"Found {len(products)} products")
        if products:
            print(f"First product: {products[0]['name']}")
    else:
        print(products_response.text)
    print("-" * 50)
    
    # 5. Test creating a product (requires seller role)
    product_data = {
        "name": f"Test Coffee {random_suffix}",
        "description": "A test coffee product",
        "price": 12.99,
        "category_id": 1,  # Assuming category ID 1 exists
        "image_url": "https://example.com/coffee.jpg",
        "is_available": True,
        "discount_percentage": 0,
        "weight": 250.0,  # Use numeric value instead of string
        "dimensions": "10x5x15cm"
    }
    
    create_product_response = requests.post(
        f"{BASE_URL}/api/products/",
        json=product_data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    
    print(f"Create Product Response: {create_product_response.status_code}")
    print(create_product_response.json() if create_product_response.status_code in [200, 201] else create_product_response.text)

if __name__ == "__main__":
    test_auth_flow()
