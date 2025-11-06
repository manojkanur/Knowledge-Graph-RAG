#!/bin/bash
# Quick setup script for macOS/Linux

echo "========================================"
echo "Knowledge Graph Demo - Setup Script"
echo "========================================"
echo

# Check Python
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi
echo "✓ Python found"
echo

# Check Docker
echo "[2/5] Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not found. Please install Docker Desktop."
    exit 1
fi
echo "✓ Docker found"
echo

# Create virtual environment
echo "[3/5] Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo

# Activate and install packages
echo "[4/5] Installing Python packages..."
source venv/bin/activate
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo "✓ Packages installed"
echo

# Start Neo4j
echo "[5/5] Starting Neo4j database..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to start Neo4j. Please check Docker is running."
    exit 1
fi
echo "✓ Neo4j started"
echo

# Check .env file
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please edit .env and add your OpenAI API key."
    echo
fi

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo
echo "Next steps:"
echo "1. Edit .env and add your OpenAI API key"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python demo.py"
echo
echo "Neo4j Browser: http://localhost:7474"
echo "  Username: neo4j"
echo "  Password: knowledge_graph_demo_2024"
echo
