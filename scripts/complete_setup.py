"""
Complete Database Setup Script
This script handles everything needed to set up the database from scratch
"""
import os
import sys
import shutil
import glob

# Add the django_backend directory to the Python path
backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'django_backend')
sys.path.insert(0, backend_path)

def clean_migrations():
    """Remove all migration files and database"""
    print("\n[Step 1/5] Cleaning old migrations and database...")
    
    # Remove database file
    db_path = os.path.join(backend_path, 'db.sqlite3')
    if os.path.exists(db_path):
        os.remove(db_path)
        print("  ✓ Removed old database")
    
    # Remove migration files from all apps
    apps = ['accounts', 'shops', 'store', 'dashboard', 'wishlist', 'orders', 
            'sellers', 'promotions', 'chat', 'refunds', 'payments']
    
    for app in apps:
        migrations_dir = os.path.join(backend_path, app, 'migrations')
        if os.path.exists(migrations_dir):
            # Keep __init__.py but remove all other migration files
            for file in glob.glob(os.path.join(migrations_dir, '*.py')):
                if not file.endswith('__init__.py'):
                    os.remove(file)
            # Remove __pycache__
            pycache_dir = os.path.join(migrations_dir, '__pycache__')
            if os.path.exists(pycache_dir):
                shutil.rmtree(pycache_dir)
    
    print("  ✓ Cleaned all migration files")

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karupatti_shop.settings')
    import django
    django.setup()

def create_migrations():
    """Create fresh migrations"""
    print("\n[Step 2/5] Creating fresh migrations...")
    from django.core.management import call_command
    
    try:
        call_command('makemigrations', interactive=False, verbosity=1)
        print("  ✓ Migrations created successfully")
        return True
    except Exception as e:
        print(f"  ✗ Error creating migrations: {e}")
        return False

def apply_migrations():
    """Apply migrations to create database tables"""
    print("\n[Step 3/5] Creating database tables...")
    from django.core.management import call_command
    
    try:
        call_command('migrate', interactive=False, verbosity=1)
        print("  ✓ Database tables created successfully")
        return True
    except Exception as e:
        print(f"  ✗ Error applying migrations: {e}")
        return False

def create_superuser():
    """Create admin superuser"""
    print("\n[Step 4/5] Creating admin superuser...")
    from django.contrib.auth import get_user_model
    
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
            print("  ✓ Superuser created")
            print("    Username: admin")
            print("    Password: admin123")
        else:
            print("  ✓ Superuser already exists")
        return True
    except Exception as e:
        print(f"  ✗ Error creating superuser: {e}")
        return False

def create_sample_data():
    """Create sample data"""
    print("\n[Step 5/5] Creating sample data...")
    from store.models import Category, Product
    from shops.models import Shop
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    try:
        # Create sample seller
        if not User.objects.filter(username='seller1').exists():
            seller = User.objects.create_user(
                username='seller1',
                email='seller@karupatti.com',
                password='seller123',
                role='seller',
                phone='9876543210'
            )
            
            # Create shop
            shop = Shop.objects.create(
                owner=seller,
                name='Traditional Karupatti Store',
                slug='traditional-karupatti-store',
                description='Authentic palm jaggery products from South India',
                is_active=True,
                is_verified=True
            )
            
            # Create categories
            cat1 = Category.objects.create(name='Palm Jaggery', slug='palm-jaggery')
            cat2 = Category.objects.create(name='Organic Products', slug='organic-products')
            cat3 = Category.objects.create(name='Traditional Sweets', slug='traditional-sweets')
            
            # Create products
            Product.objects.create(
                shop=shop,
                name='Pure Karupatti Blocks',
                slug='pure-karupatti-blocks',
                description='Traditional palm jaggery blocks made from pure palm sap.',
                price=250,
                stock=100,
                category=cat1,
                is_active=True
            )
            
            Product.objects.create(
                shop=shop,
                name='Organic Karupatti Powder',
                slug='organic-karupatti-powder',
                description='Finely ground karupatti powder, perfect for beverages.',
                price=200,
                stock=150,
                category=cat2,
                is_active=True
            )
            
            print("  ✓ Sample data created")
            print("    - Seller: seller1 / seller123")
            print("    - Shop: Traditional Karupatti Store")
            print("    - 3 categories and 2 products")
        else:
            print("  ✓ Sample data already exists")
        
        return True
    except Exception as e:
        print(f"  ✗ Error creating sample data: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 70)
    print("KARUPATTI SHOP - COMPLETE DATABASE SETUP")
    print("=" * 70)
    
    # Step 1: Clean old data
    clean_migrations()
    
    # Setup Django
    setup_django()
    
    # Step 2: Create migrations
    if not create_migrations():
        print("\n✗ Setup failed at migration creation")
        return
    
    # Step 3: Apply migrations
    if not apply_migrations():
        print("\n✗ Setup failed at migration application")
        return
    
    # Step 4: Create superuser
    if not create_superuser():
        print("\n✗ Setup failed at superuser creation")
        return
    
    # Step 5: Create sample data
    create_sample_data()
    
    # Success message
    print("\n" + "=" * 70)
    print("✓ DATABASE SETUP COMPLETE!")
    print("=" * 70)
    print("\nYour Karupatti Shop is ready to use!")
    print("\nAccess the application:")
    print("  • Homepage: http://127.0.0.1:8000/")
    print("  • Admin Panel: http://127.0.0.1:8000/admin/")
    print("\nLogin credentials:")
    print("  • Admin: admin / admin123")
    print("  • Seller: seller1 / seller123")
    print("\nNext steps:")
    print("  1. Start the server: python manage.py runserver")
    print("  2. Visit the homepage to browse products")
    print("  3. Register as a buyer or login as seller/admin")
    print("=" * 70)

if __name__ == '__main__':
    main()
