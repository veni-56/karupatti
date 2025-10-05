"""
Database Setup Script
This script creates all necessary database tables and initial data
"""
import os
import sys
import django

# Add the django_backend directory to the Python path
backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'django_backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karupatti_shop.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model

def setup_database():
    """Create database tables and initial data"""
    print("=" * 60)
    print("KARUPATTI SHOP - DATABASE SETUP")
    print("=" * 60)
    
    # Step 1: Create migrations
    print("\n[1/4] Creating migrations for all apps...")
    try:
        call_command('makemigrations', interactive=False)
        print("✓ Migrations created successfully")
    except Exception as e:
        print(f"✗ Error creating migrations: {e}")
        return False
    
    # Step 2: Run migrations
    print("\n[2/4] Applying migrations to database...")
    try:
        call_command('migrate', interactive=False)
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Error applying migrations: {e}")
        return False
    
    # Step 3: Create superuser if it doesn't exist
    print("\n[3/4] Creating admin superuser...")
    User = get_user_model()
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@karupatti.com',
                password='admin123',
                role='admin',
                phone='1234567890'
            )
            print("✓ Superuser created successfully")
            print("  Username: admin")
            print("  Password: admin123")
            print("  Email: admin@karupatti.com")
        else:
            print("✓ Superuser already exists")
    except Exception as e:
        print(f"✗ Error creating superuser: {e}")
    
    # Step 4: Create sample data
    print("\n[4/4] Creating sample data...")
    try:
        create_sample_data()
        print("✓ Sample data created successfully")
    except Exception as e:
        print(f"✗ Error creating sample data: {e}")
    
    print("\n" + "=" * 60)
    print("DATABASE SETUP COMPLETE!")
    print("=" * 60)
    print("\nYou can now:")
    print("1. Run the Django server: python manage.py runserver")
    print("2. Access admin panel: http://127.0.0.1:8000/admin/")
    print("3. Login with username 'admin' and password 'admin123'")
    print("=" * 60)
    
    return True

def create_sample_data():
    """Create sample categories and products"""
    from store.models import Category, Product
    from shops.models import Shop
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Create a sample seller
    if not User.objects.filter(username='seller1').exists():
        seller = User.objects.create_user(
            username='seller1',
            email='seller@karupatti.com',
            password='seller123',
            role='seller',
            phone='9876543210'
        )
        
        # Create a sample shop
        shop = Shop.objects.create(
            owner=seller,
            name='Traditional Karupatti Store',
            slug='traditional-karupatti-store',
            description='Authentic palm jaggery products from South India',
            is_active=True,
            is_verified=True
        )
        
        # Create categories
        categories_data = [
            {'name': 'Palm Jaggery', 'slug': 'palm-jaggery'},
            {'name': 'Organic Products', 'slug': 'organic-products'},
            {'name': 'Traditional Sweets', 'slug': 'traditional-sweets'},
            {'name': 'Health Foods', 'slug': 'health-foods'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            categories.append(category)
        
        # Create sample products
        products_data = [
            {
                'name': 'Pure Karupatti Blocks',
                'slug': 'pure-karupatti-blocks',
                'description': 'Traditional palm jaggery blocks made from pure palm sap. Rich in minerals and natural sweetness.',
                'price': 250,
                'stock': 100,
                'category': categories[0]
            },
            {
                'name': 'Organic Karupatti Powder',
                'slug': 'organic-karupatti-powder',
                'description': 'Finely ground karupatti powder, perfect for beverages and cooking.',
                'price': 200,
                'stock': 150,
                'category': categories[1]
            },
            {
                'name': 'Karupatti Coffee Mix',
                'slug': 'karupatti-coffee-mix',
                'description': 'Premium coffee blend sweetened with natural karupatti.',
                'price': 300,
                'stock': 80,
                'category': categories[3]
            },
            {
                'name': 'Traditional Karupatti Candy',
                'slug': 'traditional-karupatti-candy',
                'description': 'Handmade candies with pure karupatti and natural flavors.',
                'price': 150,
                'stock': 200,
                'category': categories[2]
            },
        ]
        
        for product_data in products_data:
            Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    'shop': shop,
                    'name': product_data['name'],
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'stock': product_data['stock'],
                    'category': product_data['category'],
                    'is_active': True
                }
            )
        
        print(f"  - Created seller account: seller1 / seller123")
        print(f"  - Created shop: {shop.name}")
        print(f"  - Created {len(categories)} categories")
        print(f"  - Created {len(products_data)} sample products")

if __name__ == '__main__':
    setup_database()
