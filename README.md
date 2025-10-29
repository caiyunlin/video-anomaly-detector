# 🎥 Video Anomaly Detection System

AI-powered surveillance video anomaly detection system based on Azure AI Foundry. Upload surveillance videos and specify anomaly detection types through custom prompts, utilizing GPT-4o for precise video content analysis.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Azure](https://img.shields.io/badge/Azure-AI%20Foundry-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Live Demo

- https://video-anomaly-detector.bravemushroom-502e9645.southeastasia.azurecontainerapps.io/

## ✨ Key Features

- 🔍 **Intelligent Anomaly Detection**: Video content analysis powered by Azure OpenAI GPT-4o
- 🎯 **Custom Detection Targets**: Specify anomaly types through custom prompts
- 📹 **Multi-format Support**: Supports MP4, AVI, MOV, MKV, WEBM video formats
- 🚀 **Containerized Deployment**: Docker-based with Azure Container Apps support
- 📊 **Real-time Analysis**: Detailed anomaly detection results with confidence scores
- 🎨 **Modern Interface**: Responsive web UI with drag-and-drop upload
- 🎬 **Demo Video Preview**: Built-in video preview for testing scenarios

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend  │    │  Flask Backend  │    │  Azure OpenAI   │
│                 │────│                 │────│                 │
│  • File Upload  │    │  • Video Process│    │  • GPT-4o Model │
│  • Result View  │    │  • Frame Extract│    │  • Anomaly Det. │
│  • Progress UI  │    │  • API Endpoints│    │  • Confidence   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 System Requirements

- **Python**: 3.11+
- **Docker**: 20.10+
- **Azure OpenAI**: GPT-4o model deployment
- **Memory**: Minimum 2GB RAM
- **Storage**: Minimum 1GB available space

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/your-username/video-anomaly-detector.git
cd video-anomaly-detector
```

### 2. Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your Azure OpenAI configuration
```

`.env` Configuration Example:
```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

### 3. Local Development

#### Option 1: Docker (Recommended)

```bash
# Windows
.\docker-run.bat

# Linux/macOS
chmod +x docker-run.sh
./docker-run.sh
```

#### Option 2: Direct Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
cd app
python app.py
```

### 4. Access Application

Open browser and visit: http://localhost:8080

## 🌐 Azure Deployment

### One-Click Deploy to Azure Container Apps

```bash
# Ensure Azure CLI is installed and logged in
az login

# Run one-click deployment script
chmod +x azure/one-click-deploy.sh
./azure/one-click-deploy.sh
```

### Manual Deployment

For detailed deployment steps, refer to:
- [PowerShell Deployment Script](azure/deploy-to-azure.ps1)
- [Bash Deployment Script](azure/deploy-to-azure.sh)
- [Kubernetes Configuration](azure/kubernetes-deployment.yaml)

## 📖 User Guide

### 1. Video Upload Options

**Upload Video File:**
- Supports drag-and-drop or click to select files
- File size limit: 50MB
- Supported formats: MP4, AVI, MOV, MKV, WEBM

**Use Demo Video:**
- 🔥 **Fire Detection Demo** - Test video for fire/smoke detection scenarios
- 🚨 **Security Incident Demo** - Test video for suspicious behavior/theft detection
- 📺 **Video Preview** - Click to preview demo videos before selection

### 2. Set Detection Instructions

Enter the anomaly types you want to detect in the "Anomaly Detection Instructions" field, for example:

```
Detect person falling or tripping behavior
```

```
Identify fire, smoke, or other security hazards
```

```
Monitor intruders or unauthorized personnel
```

### 3. Analysis Results

The system provides the following information:
- **Anomaly Status**: Whether anomalies were detected
- **Confidence Score**: Reliability of detection results (0-100%)
- **Anomaly Type**: Specific types of anomalies detected
- **Timestamps**: Specific time points when anomalies occurred
- **Detailed Description**: Detailed explanation of anomaly situations
- **Recommendations**: Suggested response actions

## 🔧 API Endpoints

### Upload and Analyze Video

```http
POST /upload
Content-Type: multipart/form-data

Parameters:
- video: Video file
- anomaly_prompt: Anomaly detection instructions
```

### Analyze Demo Video

```http
POST /analyze-demo
Content-Type: multipart/form-data

Parameters:
- demo_video: Demo video filename (video_fire.mp4 or video_thief.mp4)
- anomaly_prompt: Anomaly detection instructions
```

**Response Example:**
```json
{
  "success": true,
  "video_info": {
    "total_frames": 300,
    "fps": 30.0,
    "duration": 10.0,
    "extracted_frames": 10
  },
  "analysis": {
    "has_anomaly": true,
    "confidence_score": 0.85,
    "anomaly_type": "Person falling",
    "detected_frames": [45, 60],
    "timestamps": [1.5, 2.0],
    "description": "Detected person falling behavior at 1.5s and 2.0s",
    "recommendations": "Dispatch rescue personnel immediately"
  },
  "demo_video_used": "video_fire.mp4"
}
```

### Health Check

```http
GET /health
```

### Test Azure Connection

```http
GET /test-connection
```

## 🛠️ Development Guide

### Project Structure

```
video-anomaly-detector/
├── app/
│   ├── app.py                 # Flask main application
│   ├── azure_ai_analyzer.py   # Azure AI analysis module
│   ├── templates/
│   │   └── index.html         # Web interface template
│   └── static/
│       └── videos/            # Demo video files
├── azure/
│   ├── deploy-to-azure.ps1    # PowerShell deployment script
│   ├── deploy-to-azure.sh     # Bash deployment script
│   ├── one-click-deploy.sh    # One-click deployment script
│   └── kubernetes-deployment.yaml # K8s configuration
├── uploads/                   # Upload temporary directory
├── Dockerfile                 # Docker image configuration
├── docker-compose.yml         # Docker Compose configuration
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # Project documentation
```

### Local Development

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=development
export AZURE_OPENAI_API_KEY=your_key_here
export AZURE_OPENAI_ENDPOINT=your_endpoint_here

# Run application
cd app
python app.py
```

## 🔍 Troubleshooting

### Common Issues

1. **Azure OpenAI Connection Failure**
   - Verify API Key and Endpoint are correct
   - Confirm deployment model name matches
   - Check network connectivity

2. **Video Upload Failure**
   - Check if file format is supported
   - Ensure file size doesn't exceed 50MB
   - Verify network stability

3. **Analysis Results Anomaly**
   - Ensure prompt description is clear
   - Check video quality and clarity
   - Verify model configuration

4. **Demo Video Preview Issues**
   - Ensure browser supports HTML5 video
   - Check if demo videos exist in static/videos/
   - Verify video file permissions

### View Logs

```bash
# Docker environment logs
docker logs video-anomaly-detector -f

# Azure Container Apps logs
az containerapp logs show --name video-anomaly-detector --resource-group rg-video-anomaly-detector --follow
```

## 🤝 Contributing

Welcome to submit Issues and Pull Requests!

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Create Pull Request

## 📄 License

This project is open source under the MIT License. See [LICENSE](LICENSE) file for details.

---

**💡 Note**: Ensure to use HTTPS and appropriate security configurations in production environments.
