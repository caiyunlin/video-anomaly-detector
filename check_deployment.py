"""
Azure OpenAI 配置和部署验证工具
"""
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import json

# 加载环境变量
load_dotenv()

def check_azure_openai_config():
    """检查Azure OpenAI配置和部署"""
    print("🔍 检查 Azure OpenAI 配置...")
    print("=" * 50)
    
    # 获取配置
    api_key = os.environ.get('AZURE_OPENAI_API_KEY')
    endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
    api_version = os.environ.get('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    deployment_name = os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME')
    
    print(f"API Key: {'✅ 已设置' if api_key else '❌ 未设置'}")
    print(f"Endpoint: {endpoint}")
    print(f"API Version: {api_version}")
    print(f"Deployment Name: {deployment_name}")
    print()
    
    if not api_key or not endpoint or not deployment_name:
        print("❌ 配置不完整，请检查 .env 文件")
        return False
    
    try:
        # 初始化客户端
        print("🔗 测试连接...")
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
        
        # 测试简单请求（不使用部署）
        print("✅ 客户端初始化成功")
        
        # 测试部署是否存在
        print(f"🎯 测试部署 '{deployment_name}'...")
        
        try:
            response = client.chat.completions.create(
                model=deployment_name,  # 使用部署名称作为模型名
                messages=[
                    {"role": "user", "content": "Hello, can you respond with just 'OK'?"}
                ],
                max_tokens=10
            )
            print("✅ 部署测试成功！")
            print(f"✅ 响应: {response.choices[0].message.content}")
            return True
            
        except Exception as e:
            print(f"❌ 部署测试失败: {e}")
            
            # 提供常见的部署名称建议
            print("\n💡 常见的 GPT-4 Vision 部署名称:")
            common_names = [
                "gpt-4-vision",
                "gpt-4v",
                "gpt-4-turbo-vision",
                "gpt-4-vision-preview",
                "gpt-4o",
                "gpt-4-turbo"
            ]
            
            for name in common_names:
                print(f"   - {name}")
            
            print("\n📋 请在 Azure OpenAI Studio 中检查实际的部署名称:")
            print("   1. 登录 Azure Portal")
            print("   2. 进入您的 Azure OpenAI 资源")
            print("   3. 点击 'Model deployments' 或 '模型部署'")
            print("   4. 复制正确的部署名称到 .env 文件中")
            
            return False
            
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

def suggest_fixes():
    """提供修复建议"""
    print("\n🛠️  修复建议:")
    print("=" * 50)
    
    print("1. 检查部署名称:")
    print("   - 登录 Azure Portal → Azure OpenAI → 模型部署")
    print("   - 复制正确的部署名称")
    
    print("\n2. 常见问题:")
    print("   - 部署名称区分大小写")
    print("   - 可能是 'gpt-4o' 而不是 'gpt-4-vision-preview'")
    print("   - 新部署需要等待5分钟才能使用")
    
    print("\n3. 创建新部署:")
    print("   - 在 Azure OpenAI Studio 中创建新的 GPT-4 Vision 部署")
    print("   - 使用简单的名称如 'gpt-4-vision' 或 'gpt-4o'")

if __name__ == "__main__":
    success = check_azure_openai_config()
    if not success:
        suggest_fixes()
    
    print(f"\n{'='*50}")
    print("检查完成！" if success else "需要修复配置后重试")