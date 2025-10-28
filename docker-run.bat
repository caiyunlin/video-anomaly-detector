@echo off
REM Docker Run Startup Script - Windows

echo Docker Run - Video Anomaly Detection System
echo ==========================================

REM Check for .env file
if not exist .env (
    echo .env file not found
    echo Please copy from .env.example and configure:
    echo    copy .env.example .env
    echo    Then edit .env file to add your Azure OpenAI configuration
    pause
    exit /b 1
)

echo .env configuration file found

REM Check if Docker image exists
docker image inspect video-anomaly-detector >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker image does not exist, building...
    docker build -t video-anomaly-detector .
    if %errorlevel% neq 0 (
        echo Docker build failed
        pause
        exit /b 1
    )
)

echo Starting Docker container...
echo.
echo Startup command:
echo docker run -p 8080:8080 --env-file .env --name video-anomaly-detector video-anomaly-detector
echo.

REM Stop and remove existing container
docker stop video-anomaly-detector >nul 2>&1
docker rm video-anomaly-detector >nul 2>&1

REM Start new container
docker run -d -p 8080:8080 --env-file .env --name video-anomaly-detector video-anomaly-detector

if %errorlevel% equ 0 (
    echo Container started successfully!
    echo.
    echo Application access addresses:
    echo    - Main app: http://localhost:8080
    echo    - Config status: http://localhost:8080/config-status
    echo    - Health check: http://localhost:8080/health
    echo.
    echo Management commands:
    echo    - View logs: docker logs -f video-anomaly-detector
    echo    - Stop container: docker stop video-anomaly-detector
    echo    - Remove container: docker rm video-anomaly-detector
    echo    - Enter container: docker exec -it video-anomaly-detector bash
    echo.
    echo System started! Visit http://localhost:8080 to begin
) else (
    echo Container startup failed
    echo Check logs: docker logs video-anomaly-detector
)

pause