#!/bin/bash
# SmartStudy Planner - macOS/Linux Setup Script

echo ""
echo "========================================"
echo "  SmartStudy Planner - Setup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

# Navigate to backend
echo "[1/5] Navigating to backend directory..."
cd backend || (echo "Error: backend directory not found" && exit 1)

# Create virtual environment
echo "[2/5] Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "[4/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

# Run migrations
echo "[5/5] Setting up database..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "[ERROR] Database migration failed"
    exit 1
fi

# Create superuser (optional)
echo ""
echo "Creating superuser (optional)..."
echo "To skip, press Ctrl+C"
echo ""
python manage.py createsuperuser

echo ""
echo "========================================"
echo "   Setup Complete!"
echo "========================================"
echo ""
echo "Start the development server with:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "Then open in your browser:"
echo "   http://localhost:8001/frontend/auth.html"
echo ""
