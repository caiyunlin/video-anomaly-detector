#!/bin/bash

# Azure Video Anomaly Detector - Startup Script

set -e

echo "🚀 Starting Azure Video Anomaly Detector..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Copying from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "📋 Please edit .env file with your Azure OpenAI credentials before running the application."
    else
        echo "❌ Error: .env.example file not found. Please create .env file manually."
        exit 1
    fi
fi

# Source environment variables
if [ -f .env ]; then
    echo "📖 Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check required environment variables
required_vars=("AZURE_OPENAI_ENDPOINT")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo "❌ Error: Missing required environment variables:"
    printf '   - %s\n' "${missing_vars[@]}"
    echo "Please set these variables in your .env file."
    exit 1
fi

# Create uploads directory if it doesn't exist
mkdir -p uploads

echo "🔧 Building Docker image..."
docker-compose build

echo "🏃 Starting application..."
docker-compose up -d

echo "✅ Application started successfully!"
echo ""
echo "📍 Application URLs:"
echo "   - Main application: http://localhost:8080"
echo "   - Health check: http://localhost:8080/health"
echo "   - Test Azure connection: http://localhost:8080/test-connection"
echo ""
echo "📋 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"