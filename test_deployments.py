"""
Azure OpenAI 部署名称测试工具
"""
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# 加载环境变量
load_dotenv()

def test_deployment_name(deployment_name):
    """测试特定的部署名称"""
    api_key = os.environ.get('AZURE_OPENAI_API_KEY')
    endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
    api_version = os.environ.get('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    
    try:
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[{"role": "user", "content": "Say 'OK'"}],
            max_tokens=5
        )
        
        return True, response.choices[0].message.content
    except Exception as e:
        return False, str(e)

def main():
    print("🧪 测试常见的 GPT-4 Vision 部署名称...")
    print("=" * 50)
    
    # 常见的部署名称列表
    common_deployment_names = [
        "gpt-4o",
        "gpt-4-turbo",
        "gpt-4-vision",
        "gpt-4v",
        "gpt-4-turbo-vision", 
        "gpt-4-vision-preview",
        "gpt4-vision",
        "gpt4o",
        "gpt-4-omni"
    ]
    
    working_deployments = []
    
    for deployment_name in common_deployment_names:
        print(f"测试: {deployment_name}...", end=" ")
        success, result = test_deployment_name(deployment_name)
        
        if success:
            print(f"✅ 成功! 响应: {result}")
            working_deployments.append(deployment_name)
        else:
            if "DeploymentNotFound" in result:
                print("❌ 部署不存在")
            else:
                print(f"❌ 错误: {result[:50]}...")
    
    print("\n" + "=" * 50)
    
    if working_deployments:
        print("🎉 找到可用的部署:")
        for deployment in working_deployments:
            print(f"   ✅ {deployment}")
        
        print(f"\n💡 建议使用: {working_deployments[0]}")
        print(f"请将 .env 文件中的 AZURE_OPENAI_DEPLOYMENT_NAME 更改为: {working_deployments[0]}")
        
        # 生成更新命令
        print(f"\n📝 更新 .env 文件:")
        print(f"AZURE_OPENAI_DEPLOYMENT_NAME={working_deployments[0]}")
        
    else:
        print("❌ 没有找到可用的部署")
        print("\n💡 您需要在 Azure OpenAI Studio 中创建一个 GPT-4 Vision 部署")
        print("建议的部署配置:")
        print("   - 模型: gpt-4o (支持视觉功能)")
        print("   - 部署名称: gpt-4o")
        print("   - 版本: 最新稳定版本")

if __name__ == "__main__":
    main()