#!/bin/bash
# Build script for Render.com deployment
# Note: Tailwind CSS is pre-compiled and committed to git.

set -e  # Exit immediately if any command fails

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build complete!"
