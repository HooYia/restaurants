#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

# 1. Install Python dependencies using uv
echo "Installing Python dependencies..."
uv sync --frozen

# 2. Build frontend assets via npm (if your web portion relies on it)
echo "Installing npm packages and building assets..."
npm install
npm run build

# 3. Collect static files for production
echo "Collecting static files..."
uv run python manage.py collectstatic --noinput --ignore=input.css

# 4. Run database migrations
echo "Running database migrations..."
uv run python manage.py migrate --noinput

echo "Build process completed successfully!"
