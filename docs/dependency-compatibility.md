# Python 依赖版本兼容性指南

## 🐍 NumPy 兼容性问题

### 问题描述
```
ImportError: numpy.core.multiarray failed to import
AttributeError: _ARRAY_API not found
```

### 原因
- OpenCV 4.8.x 基于 NumPy 1.x 编译
- 默认安装的 NumPy 2.x 不向后兼容
- 需要使用兼容的版本组合

## 📦 推荐的依赖版本

### 稳定版本组合 (推荐)
```
numpy==1.24.3
opencv-python-headless==4.9.0.80
```

### 备用版本组合
```
numpy==1.26.4
opencv-python-headless==4.10.0.84
```

## 🔧 解决方案

### 方案 1: 使用固定版本 (已实现)
```bash
# 已更新 requirements.txt 使用兼容版本
pip install -r requirements.txt
```

### 方案 2: 如果仍有问题，手动降级
```bash
pip uninstall numpy opencv-python-headless -y
pip install numpy==1.24.3
pip install opencv-python-headless==4.9.0.80
```

### 方案 3: 使用约束文件
```bash
# 创建 constraints.txt
echo "numpy<2.0.0" > constraints.txt
pip install -c constraints.txt -r requirements.txt
```

## 🐳 Docker 构建修复

### 构建步骤优化
```dockerfile
# 先安装 numpy，再安装其他依赖
RUN pip install --no-deps numpy==1.24.3
RUN pip install -r requirements.txt
```

### 清理缓存重建
```bash
# 清理 Docker 缓存
docker system prune -f

# 重新构建
docker build --no-cache -t video-anomaly-detector .
```

## 📋 完整的依赖列表

### requirements.txt (当前)
```
Flask==3.0.0
opencv-python-headless==4.9.0.80
openai==1.3.7
python-dotenv==1.0.0
Pillow==10.1.0
werkzeug==3.0.1
gunicorn==21.2.0
azure-identity==1.15.0
numpy==1.24.3
```

### 版本说明
- **numpy==1.24.3**: 与 OpenCV 4.9.x 兼容的最新 1.x 版本
- **opencv-python-headless==4.9.0.80**: 支持 NumPy 1.x 的 OpenCV 版本
- **Flask==3.0.0**: 最新稳定版 Flask
- **openai==1.3.7**: 兼容的 OpenAI SDK 版本

## 🧪 测试兼容性

### 快速测试脚本
```python
#!/usr/bin/env python3
import numpy as np
import cv2
print(f"NumPy version: {np.__version__}")
print(f"OpenCV version: {cv2.__version__}")
print("✅ All imports successful!")
```

### Docker 测试
```bash
# 构建并测试
docker build -t video-anomaly-detector .
docker run --rm video-anomaly-detector python -c "import numpy, cv2; print('✅ Dependencies OK')"
```

## 🔄 版本升级路径

### 未来升级建议
1. **等待 OpenCV 5.x**: 原生支持 NumPy 2.x
2. **使用预编译轮子**: 从官方源安装兼容版本
3. **监控上游更新**: 定期检查兼容性矩阵

### 替代方案
```bash
# 如果 OpenCV 有问题，可以使用
pip install opencv-contrib-python-headless==4.9.0.80
# 或者
pip install cv2-python==4.9.0.80  # 如果可用
```

## 🚨 常见错误及解决

### 错误 1: Module compiled with NumPy 1.x
```bash
pip install "numpy<2.0.0"
pip install --force-reinstall opencv-python-headless==4.9.0.80
```

### 错误 2: No module named 'numpy.core._multiarray_umath'
```bash
pip uninstall numpy -y
pip install numpy==1.24.3
```

### 错误 3: OpenCV 导入失败
```bash
pip uninstall opencv-python opencv-python-headless -y
pip install opencv-python-headless==4.9.0.80
```

## 📝 最佳实践

1. **固定版本**: 在生产环境中始终使用固定版本
2. **测试矩阵**: 定期测试依赖兼容性
3. **Docker 层优化**: 将 NumPy 安装作为单独层
4. **CI/CD 集成**: 在管道中验证依赖兼容性