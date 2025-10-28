#!/usr/bin/env python3
"""
依赖兼容性测试脚本
测试 NumPy 和 OpenCV 的兼容性
"""

import sys
import traceback

def test_imports():
    """测试核心依赖导入"""
    print("🧪 测试 Python 依赖兼容性...")
    print("=" * 50)
    
    # 测试 NumPy
    try:
        import numpy as np
        print(f"✅ NumPy: {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy 导入失败: {e}")
        return False
    
    # 测试 OpenCV
    try:
        import cv2
        print(f"✅ OpenCV: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ OpenCV 导入失败: {e}")
        traceback.print_exc()
        return False
    
    # 测试 Flask
    try:
        import flask
        print(f"✅ Flask: {flask.__version__}")
    except ImportError as e:
        print(f"❌ Flask 导入失败: {e}")
        return False
    
    # 测试 OpenAI
    try:
        import openai
        print(f"✅ OpenAI: {openai.__version__}")
    except ImportError as e:
        print(f"❌ OpenAI 导入失败: {e}")
        return False
    
    # 测试 Azure Identity
    try:
        import azure.identity
        print("✅ Azure Identity: 已安装")
    except ImportError as e:
        print(f"❌ Azure Identity 导入失败: {e}")
        return False
    
    return True

def test_opencv_functionality():
    """测试 OpenCV 基本功能"""
    print("\n🎥 测试 OpenCV 视频功能...")
    print("=" * 50)
    
    try:
        import cv2
        import numpy as np
        
        # 创建测试图像
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        test_image[:] = (255, 0, 0)  # 蓝色图像
        
        # 测试图像编码
        ret, buffer = cv2.imencode('.jpg', test_image)
        if ret:
            print("✅ 图像编码: 成功")
        else:
            print("❌ 图像编码: 失败")
            return False
        
        # 测试 base64 编码
        import base64
        img_b64 = base64.b64encode(buffer).decode('utf-8')
        print(f"✅ Base64 编码: {len(img_b64)} 字符")
        
        print("✅ OpenCV 功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ OpenCV 功能测试失败: {e}")
        traceback.print_exc()
        return False

def test_flask_app():
    """测试 Flask 应用基本功能"""
    print("\n🌐 测试 Flask 应用组件...")
    print("=" * 50)
    
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/test')
        def test():
            return {'status': 'ok'}
        
        with app.test_client() as client:
            response = client.get('/test')
            if response.status_code == 200:
                print("✅ Flask 路由: 成功")
            else:
                print("❌ Flask 路由: 失败")
                return False
        
        print("✅ Flask 应用测试通过")
        return True
        
    except Exception as e:
        print(f"❌ Flask 应用测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 视频异常检测系统 - 依赖测试")
    print("=" * 60)
    
    print(f"Python 版本: {sys.version}")
    print()
    
    # 运行所有测试
    tests = [
        ("导入测试", test_imports),
        ("OpenCV 功能测试", test_opencv_functionality),
        ("Flask 应用测试", test_flask_app)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 运行: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    # 输出结果汇总
    print("\n" + "=" * 60)
    print("📊 测试结果汇总:")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过! 系统ready运行.")
    else:
        print("⚠️  有测试失败. 请检查依赖安装.")
        print("💡 尝试运行: pip install -r requirements.txt")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)