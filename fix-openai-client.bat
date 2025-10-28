@echo off
echo Fix Azure OpenAI Client Initialization Issue
echo ==========================================

echo Rebuilding Docker image with updated dependencies...
docker build --no-cache -t video-anomaly-detector .

if %errorlevel% equ 0 (
    echo Docker image rebuilt successfully!
    echo.
    echo Testing dependency compatibility...
    docker run --rm video-anomaly-detector python -c "from openai import AzureOpenAI; print('OpenAI library imported successfully')"
    
    if %errorlevel% equ 0 (
        echo All dependencies are working correctly!
        echo.
        echo You can now start the application using:
        echo    docker-run.bat
    ) else (
        echo Dependency test failed
    )
) else (
    echo Docker build failed
    echo Please check the error logs
)

pause