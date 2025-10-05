"""
Database Reset Script
WARNING: This will delete all data and recreate the database
"""
import os
import sys

# Add the django_backend directory to the Python path
backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'django_backend')
sys.path.insert(0, backend_path)

def reset_database():
    """Delete and recreate the database"""
    db_path = os.path.join(backend_path, 'db.sqlite3')
    
    print("=" * 60)
    print("WARNING: DATABASE RESET")
    print("=" * 60)
    print("\nThis will DELETE ALL DATA in the database!")
    
    # Delete the database file
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"✓ Deleted database file: {db_path}")
        except Exception as e:
            print(f"✗ Error deleting database: {e}")
            return False
    else:
        print("✓ No existing database found")
    
    # Delete migration files
    print("\n✓ Deleting migration files...")
    apps = ['accounts', 'shops', 'store', 'wishlist', 'orders', 'sellers', 
            'promotions', 'chat', 'refunds', 'payments', 'dashboard']
    
    for app in apps:
        migrations_dir = os.path.join(backend_path, app, 'migrations')
        if os.path.exists(migrations_dir):
            for file in os.listdir(migrations_dir):
                if file.endswith('.py') and file != '__init__.py':
                    file_path = os.path.join(migrations_dir, file)
                    try:
                        os.remove(file_path)
                        print(f"  - Deleted {app}/migrations/{file}")
                    except Exception as e:
                        print(f"  ✗ Error deleting {file}: {e}")
    
    print("\n" + "=" * 60)
    print("DATABASE RESET COMPLETE!")
    print("=" * 60)
    print("\nNext step: Run setup_database.py to recreate everything")
    print("=" * 60)

if __name__ == '__main__':
    response = input("\nAre you sure you want to reset the database? (yes/no): ")
    if response.lower() == 'yes':
        reset_database()
    else:
        print("Database reset cancelled.")
