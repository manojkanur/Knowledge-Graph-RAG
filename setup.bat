@echo off
REM Quick setup script for Windows

echo ========================================
echo Knowledge Graph Demo - Setup Script
echo ========================================
echo.

REM Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9 or higher.
    pause
    exit /b 1
)
echo ✓ Python found
echo.

REM Check Docker
echo [2/5] Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker not found. Please install Docker Desktop.
    pause
    exit /b 1
)
echo ✓ Docker found
echo.

REM Create virtual environment
echo [3/5] Creating Python virtual environment...
if not exist venv (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate and install packages
echo [4/5] Installing Python packages...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo ✓ Packages installed
echo.

REM Start Neo4j
echo [5/5] Starting Neo4j database...
docker-compose up -d
if errorlevel 1 (
    echo ERROR: Failed to start Neo4j. Please check Docker is running.
    pause
    exit /b 1
)
echo ✓ Neo4j started
echo.

REM Check .env file
if not exist .env (
    echo WARNING: .env file not found!
    echo Please edit .env and add your OpenAI API key.
    echo.
)

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env and add your OpenAI API key
echo 2. Run: python demo.py
echo.
echo Neo4j Browser: http://localhost:7474
echo   Username: neo4j
echo   Password: knowledge_graph_demo_2024
echo.
pause
