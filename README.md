# 🎥 视频异常检测系统

基于 Azure AI Foundry 的智能监控视频异常检测系统。支持上传监控视频并通过自定义 prompt 指定异常检测类型，利用 GPT-4V 进行精准的视频内容分析。

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Azure](https://img.shields.io/badge/Azure-AI%20Foundry-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ 功能特性

- 🔍 **智能异常检测**: 基于 Azure OpenAI GPT-4V 的视频内容分析
- 🎯 **自定义检测目标**: 通过 prompt 指定要检测的异常类型
- 📹 **多格式支持**: 支持 MP4, AVI, MOV, MKV, WEBM 等视频格式
- 🚀 **容器化部署**: 完全基于 Docker，支持 Azure Container Apps 部署
- 📊 **实时分析**: 提供详细的异常检测结果和置信度评分
- 🎨 **现代化界面**: 响应式 Web 界面，支持拖拽上传

## 🏗️ 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web 前端      │    │   Flask 后端    │    │  Azure OpenAI   │
│                 │────│                 │────│                 │
│  • 文件上传     │    │  • 视频处理     │    │  • GPT-4V 分析  │
│  • 结果展示     │    │  • 帧提取       │    │  • 异常检测     │
│  • 进度显示     │    │  • API 接口     │    │  • 置信度评估   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 系统要求

- **Python**: 3.11+
- **Docker**: 20.10+
- **Azure OpenAI**: GPT-4V 模型部署
- **内存**: 最低 2GB RAM
- **存储**: 最低 1GB 可用空间

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/video-anomaly-detector.git
cd video-anomaly-detector
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入您的 Azure OpenAI 配置
```

`.env` 文件配置示例：
```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4-vision-preview

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

### 3. 本地运行

#### 方式一: Docker 运行 (推荐)

```bash
# Windows
.\start.bat

# Linux/macOS
chmod +x start.sh
./start.sh
```

#### 方式二: 直接运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
cd app
python app.py
```

### 4. 访问应用

打开浏览器访问: http://localhost:8080

## 🌐 Azure 部署

### 一键部署到 Azure Container Apps

```bash
# 确保已安装并登录 Azure CLI
az login

# 运行一键部署脚本
chmod +x azure/one-click-deploy.sh
./azure/one-click-deploy.sh
```

### 手动部署

详细的部署步骤请参考：
- [PowerShell 部署脚本](azure/deploy-to-azure.ps1)
- [Bash 部署脚本](azure/deploy-to-azure.sh)
- [Kubernetes 配置](azure/kubernetes-deployment.yaml)

## 📖 使用指南

### 1. 上传视频

- 支持拖拽上传或点击选择文件
- 文件大小限制：50MB
- 支持格式：MP4, AVI, MOV, MKV, WEBM

### 2. 设置检测指令

在"异常检测指令"框中输入您想要检测的异常类型，例如：

```
检测人员跌倒或摔倒行为
```

```
识别火灾、烟雾或其他安全隐患
```

```
监测入侵者或未授权人员进入
```

### 3. 分析结果

系统将提供以下信息：
- **异常状态**: 是否检测到异常
- **置信度**: 检测结果的可信程度 (0-100%)
- **异常类型**: 具体检测到的异常类型
- **时间戳**: 异常发生的具体时间点
- **详细描述**: 异常情况的详细说明
- **建议措施**: 推荐的应对方案

## 🔧 API 接口

### 上传并分析视频

```http
POST /upload
Content-Type: multipart/form-data

Parameters:
- video: 视频文件
- anomaly_prompt: 异常检测指令
```

**响应示例:**
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
    "anomaly_type": "人员跌倒",
    "detected_frames": [45, 60],
    "timestamps": [1.5, 2.0],
    "description": "检测到人员在1.5秒和2.0秒时刻出现跌倒行为",
    "recommendations": "立即派遣救援人员"
  }
}
```

### 健康检查

```http
GET /health
```

### 测试 Azure 连接

```http
GET /test-connection
```

## 🛠️ 开发指南

### 项目结构

```
video-anomaly-detector/
├── app/
│   ├── app.py                 # Flask 主应用
│   ├── azure_ai_analyzer.py   # Azure AI 分析模块
│   ├── templates/
│   │   └── index.html         # Web 界面模板
│   └── static/                # 静态资源
├── azure/
│   ├── deploy-to-azure.ps1    # PowerShell 部署脚本
│   ├── deploy-to-azure.sh     # Bash 部署脚本
│   ├── one-click-deploy.sh    # 一键部署脚本
│   └── kubernetes-deployment.yaml # K8s 配置
├── uploads/                   # 上传文件临时目录
├── Dockerfile                 # Docker 镜像配置
├── docker-compose.yml         # Docker Compose 配置
├── requirements.txt           # Python 依赖
├── .env.example              # 环境变量模板
└── README.md                 # 项目文档
```

### 本地开发

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export FLASK_ENV=development
export AZURE_OPENAI_API_KEY=your_key_here
export AZURE_OPENAI_ENDPOINT=your_endpoint_here

# 运行应用
cd app
python app.py
```

## 🔍 故障排除

### 常见问题

1. **Azure OpenAI 连接失败**
   - 检查 API Key 和 Endpoint 是否正确
   - 确认部署模型名称是否匹配
   - 验证网络连接

2. **视频上传失败**
   - 检查文件格式是否支持
   - 确认文件大小不超过 50MB
   - 验证网络稳定性

3. **分析结果异常**
   - 确认 prompt 描述清晰
   - 检查视频质量和清晰度
   - 验证模型配置

### 日志查看

```bash
# Docker 环境日志
docker-compose logs -f

# Azure Container Apps 日志
az containerapp logs show --name video-anomaly-detector --resource-group rg-video-anomaly-detector --follow
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service/)
- [Flask](https://flask.palletsprojects.com/)
- [OpenCV](https://opencv.org/)
- [Bootstrap](https://getbootstrap.com/)

## 📧 联系我们

如有问题或建议，请通过以下方式联系：

- 📧 Email: your-email@example.com
- 🐙 GitHub Issues: [提交 Issue](https://github.com/your-username/video-anomaly-detector/issues)

---

**💡 提示**: 确保在生产环境中使用 HTTPS 和适当的安全配置。
