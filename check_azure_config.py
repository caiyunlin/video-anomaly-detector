#!/usr/bin/env python3
"""
Azure OpenAI 配置检查脚本
检查 .env 文件中的 Azure OpenAI 配置是否正确
"""

import os
import sys
from dotenv import load_dotenv

def check_env_file():
    """检查 .env 文件是否存在"""
    env_files = ['.env', '../.env']
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"✅ 找到环境配置文件: {env_file}")
            load_dotenv(env_file)
            return True
    
    print("❌ 未找到 .env 文件")
    print("💡 请从 .env.example 复制并配置:")
    print("   cp .env.example .env")
    return False

def validate_azure_config():
    """验证 Azure OpenAI 配置"""
    print("🔍 检查 Azure OpenAI 配置...")
    print("=" * 50)
    
    # 必需的配置
    required_configs = {
        'AZURE_OPENAI_ENDPOINT': {
            'value': os.environ.get('AZURE_OPENAI_ENDPOINT'),
            'description': 'Azure OpenAI 资源端点',
            'example': 'https://your-resource-name.openai.azure.com/',
            'required': True
        },
        'AZURE_OPENAI_API_KEY': {
            'value': os.environ.get('AZURE_OPENAI_API_KEY'),
            'description': 'Azure OpenAI API 密钥',
            'example': 'your-32-character-api-key',
            'required': False  # 可以使用 managed identity
        },
        'AZURE_OPENAI_DEPLOYMENT_NAME': {
            'value': os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME'),
            'description': 'GPT-4V 部署名称',
            'example': 'gpt-4-vision-preview',
            'required': True
        },
        'AZURE_OPENAI_API_VERSION': {
            'value': os.environ.get('AZURE_OPENAI_API_VERSION'),
            'description': 'API 版本',
            'example': '2024-02-15-preview',
            'required': False
        }
    }
    
    # 可选的认证配置
    optional_configs = {
        'AZURE_TENANT_ID': {
            'value': os.environ.get('AZURE_TENANT_ID'),
            'description': 'Azure 租户 ID (用于服务主体认证)',
            'example': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
        },
        'AZURE_CLIENT_ID': {
            'value': os.environ.get('AZURE_CLIENT_ID'),
            'description': 'Azure 客户端 ID (用于服务主体认证)',
            'example': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
        },
        'AZURE_CLIENT_SECRET': {
            'value': os.environ.get('AZURE_CLIENT_SECRET'),
            'description': 'Azure 客户端密钥 (用于服务主体认证)',
            'example': 'your-client-secret'
        }
    }
    
    all_good = True
    
    # 检查必需配置
    print("📋 必需配置:")
    for key, config in required_configs.items():
        value = config['value']
        
        if not value or value in ['your_endpoint_here', 'your_api_key_here', 'your-resource-name.openai.azure.com']:
            if config['required']:
                print(f"❌ {key}: 未配置或使用示例值")
                print(f"   描述: {config['description']}")
                print(f"   示例: {config['example']}")
                all_good = False
            else:
                print(f"⚠️  {key}: 未配置 (可选，可使用 managed identity)")
        else:
            # 隐藏敏感信息
            if 'KEY' in key or 'SECRET' in key:
                display_value = value[:8] + '...' + value[-4:] if len(value) > 12 else '***'
            else:
                display_value = value
            print(f"✅ {key}: {display_value}")
    
    print()
    
    # 检查可选配置
    print("🔧 可选配置 (服务主体认证):")
    sp_configured = True
    for key, config in optional_configs.items():
        value = config['value']
        
        if not value:
            print(f"⚪ {key}: 未配置")
            sp_configured = False
        else:
            if 'SECRET' in key:
                display_value = value[:4] + '...' + value[-4:] if len(value) > 8 else '***'
            else:
                display_value = value
            print(f"✅ {key}: {display_value}")
    
    if sp_configured:
        print("✅ 服务主体认证已配置")
    else:
        print("ℹ️  服务主体认证未配置 (将使用 API Key 或 managed identity)")
    
    return all_good

def test_connection():
    """测试 Azure OpenAI 连接"""
    print("\n🧪 测试 Azure OpenAI 连接...")
    print("=" * 50)
    
    try:
        # 导入必要的模块
        sys.path.append('app')
        from azure_ai_analyzer import AzureAIVideoAnalyzer
        
        # 创建分析器实例
        analyzer = AzureAIVideoAnalyzer()
        
        # 测试连接
        result = analyzer.test_connection()
        
        if result.get('success'):
            print("✅ Azure OpenAI 连接测试成功!")
            print(f"   模型: {result.get('model', 'N/A')}")
            print(f"   端点: {result.get('endpoint', 'N/A')}")
            print(f"   响应: {result.get('response', 'N/A')}")
            return True
        else:
            print("❌ Azure OpenAI 连接测试失败")
            print(f"   错误: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

def generate_config_template():
    """生成配置模板"""
    print("\n📝 生成配置模板...")
    
    template = """# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-azure-openai-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4-vision-preview

# Flask Configuration
FLASK_ENV=development
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=50000000  # 50MB max file size

# Security Configuration
SECRET_KEY=your-very-long-and-secure-secret-key-at-least-32-characters-long

# Optional: Azure Service Principal (alternative to API key)
# AZURE_TENANT_ID=your-tenant-id
# AZURE_CLIENT_ID=your-client-id
# AZURE_CLIENT_SECRET=your-client-secret
"""
    
    with open('.env.template', 'w', encoding='utf-8') as f:
        f.write(template)
    
    print("✅ 配置模板已保存到 .env.template")
    print("💡 请复制此文件为 .env 并填入您的实际配置")

def main():
    """主函数"""
    print("🔧 Azure OpenAI 配置检查工具")
    print("=" * 60)
    
    # 检查 .env 文件
    if not check_env_file():
        generate_config_template()
        return 1
    
    print()
    
    # 验证配置
    config_ok = validate_azure_config()
    
    if not config_ok:
        print("\n❌ 配置验证失败")
        print("💡 请按照上述提示修复配置问题")
        generate_config_template()
        return 1
    
    # 测试连接
    connection_ok = test_connection()
    
    print("\n" + "=" * 60)
    if config_ok and connection_ok:
        print("🎉 所有检查通过! Azure OpenAI 配置正确.")
        print("✅ 您现在可以运行视频异常检测应用了.")
    else:
        print("⚠️  配置或连接测试失败.")
        print("📖 请查看上述错误信息并修复问题.")
    
    return 0 if (config_ok and connection_ok) else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)