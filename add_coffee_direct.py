import os
from dotenv import load_dotenv
from app import create_app, db
from app.models.product import Product
from app.models.category import Category
from app.models.user import User
from flask import Flask

# Load environment variables
load_dotenv()

# Verify we're using PostgreSQL
db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
if 'postgresql' not in db_uri:
    print("ERROR: Not using PostgreSQL! Please check your .env file.")
    print(f"Current URI: {db_uri}")
    exit(1)

print(f"Using database: {db_uri}")

# Sample coffee products
COFFEE_PRODUCTS = [
    {
        "name": "Ethiopian Yirgacheffe",
        "description": "Light roast with floral and citrus notes. This Ethiopian coffee is known for its bright acidity and complex flavor profile.",
        "price": 14.99,
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
        "image_url": "https://images.unsplash.com/photo-1587734361993-0490df9a9b8b",
        "is_available": True,
        "discount_percentage": 0,
        "weight": 0.34,
        "dimensions": "8x4x2 inches"
    }
]

# Create the Flask app
app = create_app()

# Add coffee products directly to the database
with app.app_context():
    # Check if we have a seller user
    seller = User.query.filter_by(role='seller').first()
    if not seller:
        print("No seller user found. Please run add_test_user_fixed.py first.")
        exit(1)
    
    print(f"Using seller: {seller.username} (ID: {seller.id})")
    
    # Create or get coffee category
    coffee_category = Category.query.filter_by(name='Coffee Beans').first()
    if not coffee_category:
        print("Creating 'Coffee Beans' category...")
        coffee_category = Category(
            name='Coffee Beans',
            description='Premium coffee beans from around the world'
        )
        db.session.add(coffee_category)
        db.session.commit()
        print(f"Created category: Coffee Beans (ID: {coffee_category.id})")
    else:
        print(f"Using existing category: Coffee Beans (ID: {coffee_category.id})")
    
    # Add products
    for product_data in COFFEE_PRODUCTS:
        # Check if product already exists
        existing_product = Product.query.filter_by(name=product_data['name']).first()
        if existing_product:
            print(f"Product already exists: {product_data['name']} (ID: {existing_product.id})")
            continue
        
        # Create new product
        print(f"Adding product: {product_data['name']}...")
        product = Product(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            category_id=coffee_category.id,
            image_url=product_data['image_url'],
            is_available=product_data['is_available'],
            discount_percentage=product_data['discount_percentage'],
            weight=product_data['weight'],
            dimensions=product_data['dimensions']
        )
        db.session.add(product)
        db.session.commit()
        print(f"✅ Added product: {product.name} (ID: {product.id})")
    
    # List all products
    products = Product.query.all()
    print(f"\nTotal products in database: {len(products)}")
    print("ID | Name | Price | Category")
    print("-" * 50)
    for product in products:
        category_name = product.category.name if product.category else "No Category"
        print(f"{product.id} | {product.name} | ${product.price} | {category_name}")
