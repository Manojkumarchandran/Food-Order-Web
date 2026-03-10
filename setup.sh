#!/bin/bash
# ============================================
#  FoodOrder Django App - Setup Script
# ============================================

echo "🍽️  FoodOrder Setup Starting..."
echo "================================"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Load sample data
echo "🌱 Loading sample menu data..."
python manage.py loaddata restaurant/fixtures/initial_data.json

# Create superuser prompt
echo ""
echo "👤 Create admin superuser:"
python manage.py createsuperuser

# Collect static files
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Setup complete!"
echo "================================"
echo "🚀 Start server: python manage.py runserver"
echo "🔑 Admin panel: http://127.0.0.1:8000/admin/"
echo "🌐 App URL:      http://127.0.0.1:8000/"
echo "================================"
