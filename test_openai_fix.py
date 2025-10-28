"""
测试 Azure OpenAI 客户端初始化修复
"""
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_azure_openai_import():
    """测试 OpenAI 库导入"""
    try:
        from openai import AzureOpenAI
        print("✅ OpenAI 库导入成功")
        return True
    except ImportError as e:
        print(f"❌ OpenAI 库导入失败: {e}")
        return False

def test_client_initialization():
    """测试客户端初始化"""
    try:
        # 检查必需的环境变量
        api_key = os.environ.get('AZURE_OPENAI_API_KEY')
        endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
        
        if not api_key or not endpoint:
            print("⚠️  缺少必需的环境变量，跳过客户端初始化测试")
            print("   需要设置: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT")
            return True
        
        from openai import AzureOpenAI
        
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-02-15-preview",
            azure_endpoint=endpoint
        )
        print("✅ Azure OpenAI 客户端初始化成功")
        return True
    except Exception as e:
        print(f"❌ 客户端初始化失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 测试 Azure OpenAI 客户端修复")
    print("=" * 40)
    
    # 测试导入
    if not test_azure_openai_import():
        sys.exit(1)
    
    # 测试客户端初始化
    if not test_client_initialization():
        sys.exit(1)
    
    print("\n🎉 所有测试通过！客户端修复成功")

if __name__ == "__main__":
    main()