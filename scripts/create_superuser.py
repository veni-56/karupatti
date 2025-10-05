import os
import sys
import getpass

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "django_backend"))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "karupatti_shop.settings")

import django  # noqa: E402
django.setup()

from django.contrib.auth.models import User  # noqa: E402

def main():
    username = os.getenv("ADMIN_USERNAME")
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    if not username:
        username = input("Admin username: ").strip()
    if not email:
        email = input("Admin email: ").strip()
    if not password:
        password = getpass.getpass("Admin password: ").strip()
        confirm = getpass.getpass("Confirm password: ").strip()
        if password != confirm:
            print("Passwords do not match.", file=sys.stderr)
            sys.exit(1)

    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists. No changes made.")
        return

    user = User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Created superuser '{user.username}'.")

if __name__ == "__main__":
    main()
