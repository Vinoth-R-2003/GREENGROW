#!/bin/bash
# Build script for Render.com deployment
# Note: Tailwind CSS is pre-compiled and committed to git.

set -e  # Exit immediately if any command fails

echo "Installing dependencies..."
pip install -r requirements.txt

# --- TEMPORARY: WIPE DATABASE AND START FRESH ---
echo "FLUSHING DATABASE..."
python manage.py flush --no-input

echo "Creating fresh admin user (admin / admin123)..."
python -c "import os; import django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_core.settings'); django.setup(); from users.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Admin already exists')"
# -----------------------------------------------

echo "Running database migrations..."
python manage.py migrate

echo "Seeding Marketplace and Garden data..."
python seed_items.py
python seed_plants.py

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build complete!"
