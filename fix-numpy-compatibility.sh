#!/bin/bash

# 紧急修复 NumPy 兼容性问题的脚本

echo "🚨 NumPy 兼容性紧急修复脚本"
echo "=================================="

# 检查当前 Python 环境
echo "📋 检查当前 Python 环境..."
python --version
echo ""

# 检查当前依赖版本
echo "🔍 检查当前依赖版本..."
python -c "
try:
    import numpy; print(f'NumPy: {numpy.__version__}')
except: print('NumPy: 未安装')
try:
    import cv2; print(f'OpenCV: {cv2.__version__}')
except: print('OpenCV: 未安装或有问题')
"
echo ""

# 修复步骤
echo "🔧 开始修复..."

# 1. 卸载有问题的包
echo "1️⃣ 卸载有问题的包..."
pip uninstall numpy opencv-python opencv-python-headless -y

# 2. 安装兼容版本
echo "2️⃣ 安装兼容的 NumPy 版本..."
pip install numpy==1.24.3

echo "3️⃣ 安装兼容的 OpenCV 版本..."
pip install opencv-python-headless==4.9.0.80

# 3. 安装其他依赖
echo "4️⃣ 安装其他依赖..."
pip install -r requirements.txt

# 4. 验证安装
echo "5️⃣ 验证安装..."
python -c "
import numpy as np
import cv2
print(f'✅ NumPy {np.__version__} - OK')
print(f'✅ OpenCV {cv2.__version__} - OK')
print('🎉 修复完成!')
"

echo ""
echo "✅ 紧急修复完成！现在可以重新运行应用。"