# Docker 构建故障排除指南

## 🐛 常见的 Docker 构建错误及解决方案

### 1. 包依赖问题

#### 错误信息：
```
E: Package 'libgl1-mesa-glx' has no installation candidate
E: Unable to locate package libavresample-dev
```

#### 原因：
- Ubuntu 较新版本中某些包被重命名或移除
- `libgl1-mesa-glx` → `libgl1`
- `libavresample-dev` → `libswresample-dev`

#### 解决方案：
我已经更新了 Dockerfile 使用兼容的包名和 `opencv-python-headless`。

### 2. 多种 Dockerfile 选择

#### 主 Dockerfile (推荐)
```dockerfile
FROM python:3.11-slim
# 使用 opencv-python-headless 避免 GUI 依赖
```

#### 简化版 Dockerfile
如果主版本仍有问题，使用 `Dockerfile.simple`：
```bash
docker build -f Dockerfile.simple -t video-anomaly-detector .
```

### 3. OpenCV 依赖优化

#### 更改说明：
- `opencv-python` → `opencv-python-headless`
- 移除了不必要的 GUI 依赖
- 使用 `ffmpeg` 处理视频格式

### 4. 构建命令

```bash
# 主 Dockerfile
docker build -t video-anomaly-detector .

# 使用简化版
docker build -f Dockerfile.simple -t video-anomaly-detector .

# 忽略缓存重新构建
docker build --no-cache -t video-anomaly-detector .
```

### 5. 如果仍有问题

#### 方案 A: 使用预构建镜像
```dockerfile
FROM continuumio/miniconda3
```

#### 方案 B: 使用 Alpine Linux
```dockerfile
FROM python:3.11-alpine
RUN apk add --no-cache ffmpeg
```

#### 方案 C: 多阶段构建
```dockerfile
FROM python:3.11 as builder
# 构建依赖

FROM python:3.11-slim as runtime
# 运行时环境
```

## 🔧 测试构建

```bash
# 1. 清理旧镜像
docker system prune -f

# 2. 构建新镜像
docker build -t video-anomaly-detector .

# 3. 测试运行
docker run -p 8080:8080 video-anomaly-detector

# 4. 查看日志
docker logs <container-id>
```

## 📋 依赖说明

### 核心依赖：
- `opencv-python-headless`: 无 GUI 的 OpenCV
- `ffmpeg`: 视频处理库
- `libglib2.0-0`: GLib 库
- `curl`: 健康检查

### 可选依赖：
- `libsm6, libxext6, libxrender1`: X11 相关（保留以防需要）
- `libgomp1`: OpenMP 支持

## 🚀 快速修复

如果您遇到构建问题，可以使用这个最小化的 Dockerfile：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 只安装必要的依赖
RUN apt-get update && apt-get install -y ffmpeg curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY uploads/ ./uploads/

ENV PYTHONPATH=/app

EXPOSE 8080

CMD ["python", "app/app.py"]
```

保存为 `Dockerfile.minimal` 并使用：
```bash
docker build -f Dockerfile.minimal -t video-anomaly-detector .
```