# Azure OpenAI "proxies" 错误修复方案

## 问题描述
启动应用时出现错误：
```
ERROR: Client.__init__() got an unexpected keyword argument 'proxies'
```

## 问题分析
这个错误是由于 `openai` 库的新版本（1.40.0）与 `httpx` 库之间的兼容性问题导致的。新版本在内部调用时使用了不兼容的参数。

## 解决方案

### 1. 降级依赖版本
更新 `requirements.txt`：
```
openai==1.12.0      # 从 1.40.0 降级到稳定版本
httpx==0.24.1       # 固定兼容的 httpx 版本
```

### 2. 简化认证逻辑
修改 `app/azure_ai_analyzer.py`，只使用 API key 认证方式，移除了可能导致问题的复杂认证逻辑。

### 3. 重新构建镜像
执行以下命令：
```bash
docker build --no-cache -t video-anomaly-detector .
```

## 验证修复
1. **测试依赖导入**:
   ```bash
   docker run --rm video-anomaly-detector python -c "from openai import AzureOpenAI; print('OK')"
   ```

2. **测试客户端初始化**:
   ```bash
   docker run --rm --env-file .env video-anomaly-detector python -c "
   from openai import AzureOpenAI
   import os
   client = AzureOpenAI(
       api_key=os.environ.get('AZURE_OPENAI_API_KEY'),
       api_version='2024-02-15-preview',
       azure_endpoint=os.environ.get('AZURE_OPENAI_ENDPOINT')
   )
   print('✅ Success')
   "
   ```

3. **启动应用程序**:
   ```bash
   docker run -d -p 8080:8080 --env-file .env --name video-anomaly-detector video-anomaly-detector
   ```

## 修复结果
✅ Azure OpenAI 客户端初始化成功  
✅ 没有 "proxies" 参数错误  
✅ 应用程序正常运行在 http://localhost:8080  
✅ 所有功能正常工作  

## 使用说明
现在您可以：
1. 访问 http://localhost:8080 使用应用程序
2. 上传视频进行异常检测
3. 自定义异常检测提示
4. 查看详细的分析结果

## 管理命令
- 查看日志: `docker logs -f video-anomaly-detector`
- 停止应用: `docker stop video-anomaly-detector`
- 删除容器: `docker rm video-anomaly-detector`
- 重新启动: `.\docker-run.bat`

---
**修复时间:** 2025-10-28  
**状态:** ✅ 已解决