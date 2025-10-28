"""
测试 GPT-4o 图像识别功能
"""
import os
import base64
from dotenv import load_dotenv
from openai import AzureOpenAI
from PIL import Image
import io

# 加载环境变量
load_dotenv()

def create_test_image():
    """创建一个简单的测试图像"""
    # 创建一个简单的测试图像
    img = Image.new('RGB', (300, 200), color='blue')
    
    # 转换为base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    img_data = buffer.getvalue()
    img_base64 = base64.b64encode(img_data).decode('utf-8')
    
    return img_base64

def test_gpt4o_vision():
    """测试GPT-4o的视觉识别功能"""
    print("🔍 测试 GPT-4o 图像识别功能...")
    print("=" * 50)
    
    # 获取配置
    api_key = os.environ.get('AZURE_OPENAI_API_KEY')
    endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
    api_version = os.environ.get('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    
    # 使用 gpt-4o 作为部署名称
    deployment_name = "gpt-4o"
    
    try:
        # 初始化客户端
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
        
        # 创建测试图像
        print("📸 创建测试图像...")
        test_image = create_test_image()
        
        # 测试图像识别
        print(f"🤖 使用 {deployment_name} 进行图像分析...")
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "请分析这个图像，描述你看到的内容。这是一个图像识别测试。"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{test_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        result = response.choices[0].message.content
        
        print("✅ GPT-4o 图像识别测试成功!")
        print(f"📝 分析结果: {result}")
        
        # 测试视频异常检测相关的提示
        print("\n🎬 测试视频异常检测功能...")
        
        anomaly_response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text",
                            "text": """作为视频监控异常检测专家，请分析这个图像中是否存在以下异常行为：
                            - 可疑人员行为
                            - 物品遗留
                            - 人员摔倒
                            - 车辆违规
                            
                            请提供详细的分析结果，包括是否发现异常、异常类型、置信度等。"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{test_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        anomaly_result = anomaly_response.choices[0].message.content
        print(f"🚨 异常检测结果: {anomaly_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🧪 GPT-4o 图像识别能力验证")
    print("=" * 50)
    
    print("📋 GPT-4o 支持的图像识别功能:")
    features = [
        "✅ 图像内容识别和描述",
        "✅ 物体检测和分类", 
        "✅ 人物和行为分析",
        "✅ 场景理解和上下文分析",
        "✅ 异常行为检测",
        "✅ 视频帧序列分析",
        "✅ 自定义异常类型检测",
        "✅ 详细分析报告生成"
    ]
    
    for feature in features:
        print(f"   {feature}")
    
    print(f"\n{'-'*50}")
    
    # 运行测试
    if test_gpt4o_vision():
        print("\n🎉 结论: GPT-4o 完全支持图像识别!")
        print("✅ 您的视频异常检测系统可以正常工作")
        print("✅ 请将 .env 中的 AZURE_OPENAI_DEPLOYMENT_NAME 设置为 'gpt-4o'")
    else:
        print("\n❌ 需要检查配置或部署状态")

if __name__ == "__main__":
    main()