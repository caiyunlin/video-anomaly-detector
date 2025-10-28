#!/bin/bash

# One-click deployment script for Azure Container Apps
# This script will prompt for necessary information and deploy the application

echo "🚀 Azure Video Anomaly Detector - One-Click Deployment"
echo "======================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists az; then
    echo "❌ Azure CLI is not installed. Please install it first:"
    echo "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

if ! az account show >/dev/null 2>&1; then
    echo "❌ Please log in to Azure CLI first:"
    echo "   az login"
    exit 1
fi

echo "✅ Prerequisites check passed!"
echo ""

# Get user input
echo "📝 Please provide the following information:"
echo ""

read -p "🌍 Azure region (default: eastus): " LOCATION
LOCATION=${LOCATION:-eastus}

read -p "📋 Resource group name (default: rg-video-anomaly-detector): " RESOURCE_GROUP_NAME
RESOURCE_GROUP_NAME=${RESOURCE_GROUP_NAME:-rg-video-anomaly-detector}

read -p "🔗 Azure OpenAI Endpoint (e.g., https://your-openai.openai.azure.com/): " AZURE_OPENAI_ENDPOINT
if [[ -z "$AZURE_OPENAI_ENDPOINT" ]]; then
    echo "❌ Azure OpenAI Endpoint is required!"
    exit 1
fi

read -s -p "🔑 Azure OpenAI API Key: " AZURE_OPENAI_API_KEY
echo ""
if [[ -z "$AZURE_OPENAI_API_KEY" ]]; then
    echo "❌ Azure OpenAI API Key is required!"
    exit 1
fi

read -p "🤖 Azure OpenAI Deployment Name (default: gpt-4-vision-preview): " AZURE_OPENAI_DEPLOYMENT_NAME
AZURE_OPENAI_DEPLOYMENT_NAME=${AZURE_OPENAI_DEPLOYMENT_NAME:-gpt-4-vision-preview}

echo ""
echo "📋 Deployment Summary:"
echo "   Region: $LOCATION"
echo "   Resource Group: $RESOURCE_GROUP_NAME"
echo "   OpenAI Endpoint: $AZURE_OPENAI_ENDPOINT"
echo "   Deployment Name: $AZURE_OPENAI_DEPLOYMENT_NAME"
echo ""

read -p "Do you want to proceed with deployment? (y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled."
    exit 1
fi

# Set deployment variables
CONTAINER_APP_ENV_NAME="env-video-anomaly-detector"
CONTAINER_APP_NAME="video-anomaly-detector"
CONTAINER_REGISTRY_NAME="acrvideoanomaly$RANDOM"
LOG_ANALYTICS_WORKSPACE="law-video-anomaly-detector"

echo ""
echo "🚀 Starting deployment..."

# Create resource group
echo "📋 Creating resource group..."
az group create \
    --name "$RESOURCE_GROUP_NAME" \
    --location "$LOCATION" \
    --output table

# Create Azure Container Registry
echo "📦 Creating Azure Container Registry..."
az acr create \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --name "$CONTAINER_REGISTRY_NAME" \
    --sku Basic \
    --admin-enabled true \
    --output table

# Build and push Docker image
echo "🔨 Building and pushing Docker image (this may take a few minutes)..."
az acr build \
    --registry "$CONTAINER_REGISTRY_NAME" \
    --image video-anomaly-detector:latest \
    --file Dockerfile \
    . \
    --output table

# Create Log Analytics workspace
echo "📊 Creating Log Analytics workspace..."
az monitor log-analytics workspace create \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --workspace-name "$LOG_ANALYTICS_WORKSPACE" \
    --location "$LOCATION" \
    --output table

# Get workspace details
LOG_ANALYTICS_WORKSPACE_ID=$(az monitor log-analytics workspace show \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --workspace-name "$LOG_ANALYTICS_WORKSPACE" \
    --query customerId \
    --output tsv)

LOG_ANALYTICS_KEY=$(az monitor log-analytics workspace get-shared-keys \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --workspace-name "$LOG_ANALYTICS_WORKSPACE" \
    --query primarySharedKey \
    --output tsv)

# Create Container Apps environment
echo "🌐 Creating Container Apps environment..."
az containerapp env create \
    --name "$CONTAINER_APP_ENV_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --location "$LOCATION" \
    --logs-workspace-id "$LOG_ANALYTICS_WORKSPACE_ID" \
    --logs-workspace-key "$LOG_ANALYTICS_KEY" \
    --output table

# Get ACR details
ACR_LOGIN_SERVER=$(az acr show \
    --name "$CONTAINER_REGISTRY_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --query loginServer \
    --output tsv)

# Create Container App
echo "🚀 Creating Container App..."
az containerapp create \
    --name "$CONTAINER_APP_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --environment "$CONTAINER_APP_ENV_NAME" \
    --image "$ACR_LOGIN_SERVER/video-anomaly-detector:latest" \
    --registry-server "$ACR_LOGIN_SERVER" \
    --target-port 8080 \
    --ingress external \
    --cpu 1.0 \
    --memory 2.0Gi \
    --min-replicas 1 \
    --max-replicas 5 \
    --env-vars \
        "AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT" \
        "AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY" \
        "AZURE_OPENAI_DEPLOYMENT_NAME=$AZURE_OPENAI_DEPLOYMENT_NAME" \
        "AZURE_OPENAI_API_VERSION=2024-02-15-preview" \
        "FLASK_ENV=production" \
    --output table

# Get the application URL
APP_URL=$(az containerapp show \
    --name "$CONTAINER_APP_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --query properties.configuration.ingress.fqdn \
    --output tsv)

echo ""
echo "✅ Deployment completed successfully!"
echo "======================================="
echo ""
echo "🌐 Application URL: https://$APP_URL"
echo "📊 Health Check: https://$APP_URL/health"
echo "🔧 Test Connection: https://$APP_URL/test-connection"
echo ""
echo "📋 Resource Information:"
echo "   Resource Group: $RESOURCE_GROUP_NAME"
echo "   Container Registry: $CONTAINER_REGISTRY_NAME"
echo "   Container App: $CONTAINER_APP_NAME"
echo "   Environment: $CONTAINER_APP_ENV_NAME"
echo ""
echo "📝 Useful Commands:"
echo "   View logs: az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP_NAME --follow"
echo "   Update app: az containerapp update --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP_NAME --image $ACR_LOGIN_SERVER/video-anomaly-detector:latest"
echo "   Delete resources: az group delete --name $RESOURCE_GROUP_NAME"
echo ""
echo "🎉 Your video anomaly detection application is now running in Azure!"