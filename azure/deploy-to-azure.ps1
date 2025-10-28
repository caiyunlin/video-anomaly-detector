# Azure Container Apps Deployment Configuration
# This file contains the Azure CLI commands to deploy the video anomaly detector to Azure Container Apps

# Set variables
$RESOURCE_GROUP_NAME = "rg-video-anomaly-detector"
$LOCATION = "East US"
$CONTAINER_APP_ENV_NAME = "env-video-anomaly-detector"
$CONTAINER_APP_NAME = "video-anomaly-detector"
$CONTAINER_REGISTRY_NAME = "acrvideoanomaly$(Get-Random -Minimum 1000 -Maximum 9999)"
$LOG_ANALYTICS_WORKSPACE = "law-video-anomaly-detector"

# Azure OpenAI Configuration (Update these with your actual values)
$AZURE_OPENAI_ENDPOINT = "https://your-openai-resource.openai.azure.com/"
$AZURE_OPENAI_API_KEY = "your-api-key-here"
$AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4-vision-preview"

Write-Host "🚀 Starting Azure Container Apps deployment..." -ForegroundColor Green

# 1. Create resource group
Write-Host "📋 Creating resource group..." -ForegroundColor Yellow
az group create `
    --name $RESOURCE_GROUP_NAME `
    --location $LOCATION

# 2. Create Azure Container Registry
Write-Host "📦 Creating Azure Container Registry..." -ForegroundColor Yellow
az acr create `
    --resource-group $RESOURCE_GROUP_NAME `
    --name $CONTAINER_REGISTRY_NAME `
    --sku Basic `
    --admin-enabled true

# 3. Build and push Docker image to ACR
Write-Host "🔨 Building and pushing Docker image..." -ForegroundColor Yellow
az acr build `
    --registry $CONTAINER_REGISTRY_NAME `
    --image video-anomaly-detector:latest `
    --file Dockerfile `
    .

# 4. Create Log Analytics workspace
Write-Host "📊 Creating Log Analytics workspace..." -ForegroundColor Yellow
az monitor log-analytics workspace create `
    --resource-group $RESOURCE_GROUP_NAME `
    --workspace-name $LOG_ANALYTICS_WORKSPACE `
    --location $LOCATION

# 5. Get Log Analytics workspace ID and key
$LOG_ANALYTICS_WORKSPACE_ID = az monitor log-analytics workspace show `
    --resource-group $RESOURCE_GROUP_NAME `
    --workspace-name $LOG_ANALYTICS_WORKSPACE `
    --query customerId `
    --output tsv

$LOG_ANALYTICS_KEY = az monitor log-analytics workspace get-shared-keys `
    --resource-group $RESOURCE_GROUP_NAME `
    --workspace-name $LOG_ANALYTICS_WORKSPACE `
    --query primarySharedKey `
    --output tsv

# 6. Create Container Apps environment
Write-Host "🌐 Creating Container Apps environment..." -ForegroundColor Yellow
az containerapp env create `
    --name $CONTAINER_APP_ENV_NAME `
    --resource-group $RESOURCE_GROUP_NAME `
    --location $LOCATION `
    --logs-workspace-id $LOG_ANALYTICS_WORKSPACE_ID `
    --logs-workspace-key $LOG_ANALYTICS_KEY

# 7. Get ACR login server and credentials
$ACR_LOGIN_SERVER = az acr show `
    --name $CONTAINER_REGISTRY_NAME `
    --resource-group $RESOURCE_GROUP_NAME `
    --query loginServer `
    --output tsv

$ACR_USERNAME = az acr credential show `
    --name $CONTAINER_REGISTRY_NAME `
    --resource-group $RESOURCE_GROUP_NAME `
    --query username `
    --output tsv

$ACR_PASSWORD = az acr credential show `
    --name $CONTAINER_REGISTRY_NAME `
    --resource-group $RESOURCE_GROUP_NAME `
    --query passwords[0].value `
    --output tsv

# 8. Create Container App
Write-Host "🚀 Creating Container App..." -ForegroundColor Yellow
az containerapp create `
    --name $CONTAINER_APP_NAME `
    --resource-group $RESOURCE_GROUP_NAME `
    --environment $CONTAINER_APP_ENV_NAME `
    --image "$ACR_LOGIN_SERVER/video-anomaly-detector:latest" `
    --registry-server $ACR_LOGIN_SERVER `
    --registry-username $ACR_USERNAME `
    --registry-password $ACR_PASSWORD `
    --target-port 8080 `
    --ingress external `
    --cpu 1.0 `
    --memory 2.0Gi `
    --min-replicas 1 `
    --max-replicas 3 `
    --env-vars "AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT" "AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY" "AZURE_OPENAI_DEPLOYMENT_NAME=$AZURE_OPENAI_DEPLOYMENT_NAME" "AZURE_OPENAI_API_VERSION=2024-02-15-preview" "FLASK_ENV=production"

# 9. Get the application URL
$APP_URL = az containerapp show `
    --name $CONTAINER_APP_NAME `
    --resource-group $RESOURCE_GROUP_NAME `
    --query properties.configuration.ingress.fqdn `
    --output tsv

Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
Write-Host "🌐 Application URL: https://$APP_URL" -ForegroundColor Cyan
Write-Host "📊 Health Check: https://$APP_URL/health" -ForegroundColor Cyan
Write-Host "🔧 Test Connection: https://$APP_URL/test-connection" -ForegroundColor Cyan

Write-Host "`n📋 Resource Information:" -ForegroundColor Yellow
Write-Host "   Resource Group: $RESOURCE_GROUP_NAME" -ForegroundColor White
Write-Host "   Container Registry: $CONTAINER_REGISTRY_NAME" -ForegroundColor White
Write-Host "   Container App: $CONTAINER_APP_NAME" -ForegroundColor White
Write-Host "   Environment: $CONTAINER_APP_ENV_NAME" -ForegroundColor White