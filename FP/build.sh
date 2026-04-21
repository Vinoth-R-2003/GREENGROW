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

echo "Build complete!"
