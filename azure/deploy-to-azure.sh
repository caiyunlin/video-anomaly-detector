#!/bin/bash

# Azure Container Apps Deployment Script
# This script deploys the video anomaly detector to Azure Container Apps

set -e

# Set variables
RESOURCE_GROUP_NAME="rg-video-anomaly-detector"
LOCATION="East US"
CONTAINER_APP_ENV_NAME="env-video-anomaly-detector"
CONTAINER_APP_NAME="video-anomaly-detector"
CONTAINER_REGISTRY_NAME="acrvideoanomaly$RANDOM"
LOG_ANALYTICS_WORKSPACE="law-video-anomaly-detector"

# Azure OpenAI Configuration (Update these with your actual values)
AZURE_OPENAI_ENDPOINT="https://your-openai-resource.openai.azure.com/"
AZURE_OPENAI_API_KEY="your-api-key-here"
AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4-vision-preview"

echo "🚀 Starting Azure Container Apps deployment..."

# Check if Azure CLI is installed and logged in
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first."
    exit 1
fi

# Check if logged in to Azure
if ! az account show &> /dev/null; then
    echo "❌ Please log in to Azure CLI first: az login"
    exit 1
fi

# 1. Create resource group
echo "📋 Creating resource group..."
az group create \
    --name $RESOURCE_GROUP_NAME \
    --location "$LOCATION"

# 2. Create Azure Container Registry
echo "📦 Creating Azure Container Registry..."
az acr create \
    --resource-group $RESOURCE_GROUP_NAME \
    --name $CONTAINER_REGISTRY_NAME \
    --sku Basic \
    --admin-enabled true

# 3. Build and push Docker image to ACR
echo "🔨 Building and pushing Docker image..."
az acr build \
    --registry $CONTAINER_REGISTRY_NAME \
    --image video-anomaly-detector:latest \
    --file Dockerfile \
    .

# 4. Create Log Analytics workspace
echo "📊 Creating Log Analytics workspace..."
az monitor log-analytics workspace create \
    --resource-group $RESOURCE_GROUP_NAME \
    --workspace-name $LOG_ANALYTICS_WORKSPACE \
    --location "$LOCATION"

# 5. Get Log Analytics workspace ID and key
LOG_ANALYTICS_WORKSPACE_ID=$(az monitor log-analytics workspace show \
    --resource-group $RESOURCE_GROUP_NAME \
    --workspace-name $LOG_ANALYTICS_WORKSPACE \
    --query customerId \
    --output tsv)

LOG_ANALYTICS_KEY=$(az monitor log-analytics workspace get-shared-keys \
    --resource-group $RESOURCE_GROUP_NAME \
    --workspace-name $LOG_ANALYTICS_WORKSPACE \
    --query primarySharedKey \
    --output tsv)

# 6. Create Container Apps environment
echo "🌐 Creating Container Apps environment..."
az containerapp env create \
    --name $CONTAINER_APP_ENV_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --location "$LOCATION" \
    --logs-workspace-id $LOG_ANALYTICS_WORKSPACE_ID \
    --logs-workspace-key $LOG_ANALYTICS_KEY

# 7. Get ACR login server and credentials
ACR_LOGIN_SERVER=$(az acr show \
    --name $CONTAINER_REGISTRY_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --query loginServer \
    --output tsv)

ACR_USERNAME=$(az acr credential show \
    --name $CONTAINER_REGISTRY_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --query username \
    --output tsv)

ACR_PASSWORD=$(az acr credential show \
    --name $CONTAINER_REGISTRY_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --query passwords[0].value \
    --output tsv)

# 8. Create Container App
echo "🚀 Creating Container App..."
az containerapp create \
    --name $CONTAINER_APP_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --environment $CONTAINER_APP_ENV_NAME \
    --image "$ACR_LOGIN_SERVER/video-anomaly-detector:latest" \
    --registry-server $ACR_LOGIN_SERVER \
    --registry-username $ACR_USERNAME \
    --registry-password "$ACR_PASSWORD" \
    --target-port 8080 \
    --ingress external \
    --cpu 1.0 \
    --memory 2.0Gi \
    --min-replicas 1 \
    --max-replicas 3 \
    --env-vars "AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT" "AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY" "AZURE_OPENAI_DEPLOYMENT_NAME=$AZURE_OPENAI_DEPLOYMENT_NAME" "AZURE_OPENAI_API_VERSION=2024-02-15-preview" "FLASK_ENV=production"

# 9. Get the application URL
APP_URL=$(az containerapp show \
    --name $CONTAINER_APP_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --query properties.configuration.ingress.fqdn \
    --output tsv)

echo "✅ Deployment completed successfully!"
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
echo "📝 Next steps:"
echo "1. Update the Azure OpenAI configuration in the script with your actual values"
echo "2. Test the application using the provided URLs"
echo "3. Monitor logs: az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP_NAME"