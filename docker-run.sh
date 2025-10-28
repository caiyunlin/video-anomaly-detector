#!/bin/bash

# Docker Run 启动脚本 - Linux/macOS

echo "🐳 使用 Docker Run 启动视频异常检测系统"
echo "========================================="

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "❌ 未找到 .env 文件"
    echo "💡 请从 .env.example 复制并配置:"
    echo "   cp .env.example .env"
    echo "   然后编辑 .env 文件填入您的 Azure OpenAI 配置"
    exit 1
fi

echo "✅ 找到 .env 配置文件"

# 检查 Docker 镜像是否存在
if ! docker image inspect video-anomaly-detector >/dev/null 2>&1; then
    echo "📦 Docker 镜像不存在，开始构建..."
    docker build -t video-anomaly-detector .
    if [ $? -ne 0 ]; then
        echo "❌ Docker 构建失败"
        exit 1
    fi
fi

echo "🚀 启动 Docker 容器..."
echo ""
echo "📋 启动命令:"
echo "docker run -p 8080:8080 --env-file .env --name video-anomaly-detector video-anomaly-detector"
echo ""

# 停止并删除已存在的容器
docker stop video-anomaly-detector >/dev/null 2>&1
docker rm video-anomaly-detector >/dev/null 2>&1

# 启动新容器
docker run -d -p 8080:8080 --env-file .env --name video-anomaly-detector video-anomaly-detector

if [ $? -eq 0 ]; then
    echo "✅ 容器启动成功!"
    echo ""
    echo "📍 应用程序访问地址:"
    echo "   - 主应用: http://localhost:8080"
    echo "   - 配置状态: http://localhost:8080/config-status"
    echo "   - 健康检查: http://localhost:8080/health"
    echo ""
    echo "📋 管理命令:"
    echo "   - 查看日志: docker logs -f video-anomaly-detector"
    echo "   - 停止容器: docker stop video-anomaly-detector"
    echo "   - 删除容器: docker rm video-anomaly-detector"
    echo "   - 进入容器: docker exec -it video-anomaly-detector bash"
    echo ""
    echo "🎉 系统已启动! 请访问 http://localhost:8080 开始使用"
else
    echo "❌ 容器启动失败"
    echo "📋 请检查日志: docker logs video-anomaly-detector"
fi