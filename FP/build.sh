#!/bin/bash
# Build script for Render.com deployment
# Note: Tailwind CSS is pre-compiled and committed to git.
# Node.js is not available in Render's Python environment.

set -e  # Exit immediately if any command fails

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Seeding Marketplace and Garden data..."
python seed_items.py
python seed_plants.py

echo "Checking Cloudinary configuration..."
python -c "import os; cn = os.environ.get('CLOUDINARY_CLOUD_NAME',''); print('[OK] CLOUDINARY_CLOUD_NAME is SET (' + cn[:4] + '...)') if cn else print('[WARNING] CLOUDINARY_CLOUD_NAME is NOT SET')"

echo "Build complete!"
