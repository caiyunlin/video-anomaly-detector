@echo off
REM Azure Video Anomaly Detector - Startup Script for Windows

echo 🚀 Starting Azure Video Anomaly Detector...

REM Check if .env file exists
if not exist .env (
    echo ⚠️  Warning: .env file not found. Copying from .env.example...
    if exist .env.example (
        copy .env.example .env
        echo 📋 Please edit .env file with your Azure OpenAI credentials before running the application.
        pause
    ) else (
        echo ❌ Error: .env.example file not found. Please create .env file manually.
        pause
        exit /b 1
    )
)

REM Create uploads directory if it doesn't exist
if not exist uploads mkdir uploads

echo 🔧 Building Docker image (with dependency fixes)...
docker-compose build --no-cache

echo 🧪 Testing dependencies...
docker run --rm video-anomaly-detector python test_dependencies.py

echo 🏃 Starting application...
docker-compose up -d

echo ✅ Application started successfully!
echo.
echo 📍 Application URLs:
echo    - Main application: http://localhost:8080
echo    - Configuration status: http://localhost:8080/config-status  
echo    - Health check: http://localhost:8080/health
echo    - Test Azure connection: http://localhost:8080/test-connection
echo.
echo 📋 To view logs: docker-compose logs -f
echo 🛑 To stop: docker-compose down
echo.
pause