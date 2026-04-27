#!/bin/bash
# Build script for Render.com deployment
# Note: Tailwind CSS is pre-compiled and committed to git.

set -e  # Exit immediately if any command fails

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running database migrations..."
python manage.py migrate

echo "Seeding Marketplace and Garden data..."
python seed_items.py
python seed_plants.py

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build complete!"
