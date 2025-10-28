# 使用示例和最佳实践

## 异常检测 Prompt 示例

### 🚨 安全监控

#### 人员安全
```
检测人员跌倒、摔倒或突然倒地的行为
```

```
识别人员之间的冲突、打斗或暴力行为
```

```
监测人员是否正确佩戴安全帽和防护设备
```

#### 入侵检测
```
检测未授权人员进入限制区域
```

```
识别翻越围栏、攀爬或非正常进入行为
```

```
监测夜间或非工作时间的异常人员活动
```

### 🔥 火灾和危险品监控

```
检测火焰、烟雾或燃烧迹象
```

```
识别危险化学品泄漏或异常气体释放
```

```
监测高温设备异常或过热现象
```

### 🚗 交通监控

```
检测车辆违规停车或占用应急通道
```

```
识别交通事故或车辆碰撞
```

```
监测行人违规穿越或在危险区域活动
```

### 🏭 工业安全

```
检测设备异常运转或故障迹象
```

```
识别生产线上的产品缺陷或异常
```

```
监测工作人员是否遵循安全操作规程
```

### 🏪 零售监控

```
检测顾客的异常行为或可疑活动
```

```
识别商品被盗或破坏行为
```

```
监测店内人流聚集或拥挤情况
```

## 最佳实践建议

### 📝 Prompt 编写技巧

1. **具体明确**: 详细描述要检测的异常类型
   - ❌ 不好: "检测异常"
   - ✅ 好: "检测人员在工作区域内跌倒或摔倒"

2. **包含上下文**: 提供场景信息有助于提高准确性
   - ✅ "在生产车间监测工人是否正确佩戴安全帽"
   - ✅ "在停车场检测车辆违规停放在消防通道"

3. **多重条件**: 可以同时检测多种异常
   - ✅ "检测火灾、烟雾或其他安全隐患，包括异常高温或化学品泄漏"

4. **避免主观判断**: 专注于可观察的行为
   - ❌ 不好: "检测可疑人员"
   - ✅ 好: "检测人员长时间逗留或在非开放时间活动"

### 🎥 视频质量要求

#### 推荐规格
- **分辨率**: 720p (1280x720) 或更高
- **帧率**: 15-30 FPS
- **时长**: 建议 5-60 秒
- **格式**: MP4 (H.264 编码) 推荐
- **文件大小**: 小于 50MB

#### 质量优化
- 确保充足的光照条件
- 避免剧烈的摄像头抖动
- 保持关键区域在画面中央
- 减少背景噪音和干扰

### ⚡ 性能优化

#### 视频预处理
```python
# 示例：压缩视频以提高处理速度
import cv2

def compress_video(input_path, output_path, target_width=720):
    cap = cv2.VideoCapture(input_path)
    
    # 获取原始视频属性
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 计算新的尺寸
    if width > target_width:
        new_width = target_width
        new_height = int(height * (target_width / width))
    else:
        new_width, new_height = width, height
    
    # 设置输出视频编码器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # 调整帧大小
        if width > target_width:
            frame = cv2.resize(frame, (new_width, new_height))
        
        out.write(frame)
    
    cap.release()
    out.release()
```

#### 帧采样策略
- 短视频 (< 10秒): 每秒采样 1-2 帧
- 中等视频 (10-30秒): 每 2-3 秒采样 1 帧
- 长视频 (> 30秒): 均匀采样 10-15 帧

### 🔧 配置调优

#### Azure OpenAI 参数
```python
# 推荐配置
{
    "temperature": 0.1,      # 低温度获得更一致的结果
    "max_tokens": 2000,      # 足够的令牌数获取详细分析
    "top_p": 0.9,           # 适中的 top_p 值
}
```

#### 容器资源配置
```yaml
# Azure Container Apps 推荐配置
resources:
  requests:
    cpu: "1.0"
    memory: "2Gi"
  limits:
    cpu: "2.0" 
    memory: "4Gi"
```

## 常见场景配置

### 🏢 办公楼监控

**检测目标**: 人员安全、入侵检测
**推荐 Prompt**:
```
监测办公区域内人员跌倒、冲突或未授权人员进入，
特别关注非工作时间的异常活动
```

**配置建议**:
- 置信度阈值: 70%
- 采样间隔: 2秒
- 最大分析帧数: 10

### 🏭 工厂车间

**检测目标**: 工业安全、设备监控
**推荐 Prompt**:
```
检测生产车间内工人违反安全规程，包括未佩戴防护装备、
进入危险区域或设备异常运转
```

**配置建议**:
- 置信度阈值: 80%
- 采样间隔: 1秒
- 最大分析帧数: 15

### 🏪 商业场所

**检测目标**: 安全防范、行为监控
**推荐 Prompt**:
```
识别商店内顾客的异常行为，包括商品盗窃、破坏行为
或人群聚集造成的安全隐患
```

**配置建议**:
- 置信度阈值: 75%
- 采样间隔: 1.5秒
- 最大分析帧数: 12

## 集成示例

### 与警报系统集成

```python
import requests
import json

def send_alert(analysis_result):
    """发送警报到监控中心"""
    if analysis_result['has_anomaly'] and analysis_result['confidence_score'] > 0.8:
        alert_data = {
            'type': 'video_anomaly',
            'severity': 'high' if analysis_result['confidence_score'] > 0.9 else 'medium',
            'description': analysis_result['description'],
            'timestamp': time.time(),
            'confidence': analysis_result['confidence_score']
        }
        
        # 发送到警报系统
        response = requests.post(
            'https://your-alert-system.com/api/alerts',
            json=alert_data,
            headers={'Authorization': 'Bearer your-token'}
        )
        
        return response.status_code == 200
    
    return False
```

### 与数据库集成

```python
import sqlite3
from datetime import datetime

def save_analysis_result(video_file, analysis_result):
    """保存分析结果到数据库"""
    conn = sqlite3.connect('anomaly_detection.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO analysis_results 
        (video_file, has_anomaly, confidence_score, anomaly_type, description, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        video_file,
        analysis_result['has_anomaly'],
        analysis_result['confidence_score'],
        analysis_result.get('anomaly_type', ''),
        analysis_result['description'],
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()
```

## 故障排除指南

### 分析准确性问题

1. **置信度过低**
   - 检查视频质量和清晰度
   - 优化 prompt 描述
   - 确保目标行为在画面中清晰可见

2. **误报率过高**
   - 提高置信度阈值
   - 细化 prompt 描述
   - 增加上下文信息

3. **漏报情况**
   - 降低置信度阈值
   - 增加采样帧数
   - 优化视频质量

### 性能优化

1. **处理速度慢**
   - 压缩视频文件
   - 减少采样帧数
   - 使用更高性能的 Azure 实例

2. **内存使用过高**
   - 限制最大文件大小
   - 优化帧提取算法
   - 增加容器内存配置

通过遵循这些最佳实践，您可以获得更准确、更可靠的视频异常检测结果。