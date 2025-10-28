@echo off
REM Azure OpenAI 配置检查脚本 (Windows)

echo 🔧 Azure OpenAI 配置检查工具
echo ============================================

REM 检查 .env 文件是否存在
if exist .env (
    echo ✅ 找到 .env 配置文件
) else (
    echo ❌ 未找到 .env 文件
    echo 💡 请从 .env.example 复制并配置:
    echo    copy .env.example .env
    echo    然后编辑 .env 文件填入您的 Azure OpenAI 配置
    pause
    exit /b 1
)

echo.
echo 🔍 检查 .env 文件内容...
echo ============================================

REM 检查必需的配置项
findstr /C:"AZURE_OPENAI_ENDPOINT=" .env >nul
if %errorlevel% equ 0 (
    echo ✅ 找到 AZURE_OPENAI_ENDPOINT 配置
    for /f "tokens=2 delims==" %%a in ('findstr /C:"AZURE_OPENAI_ENDPOINT=" .env') do (
        if "%%a"=="https://your-resource-name.openai.azure.com/" (
            echo ❌ AZURE_OPENAI_ENDPOINT 仍使用示例值，请替换为您的实际端点
        ) else (
            echo    端点: %%a
        )
    )
) else (
    echo ❌ 未找到 AZURE_OPENAI_ENDPOINT 配置
)

findstr /C:"AZURE_OPENAI_API_KEY=" .env >nul
if %errorlevel% equ 0 (
    echo ✅ 找到 AZURE_OPENAI_API_KEY 配置
    for /f "tokens=2 delims==" %%a in ('findstr /C:"AZURE_OPENAI_API_KEY=" .env') do (
        if "%%a"=="your_azure_openai_api_key_here" (
            echo ❌ AZURE_OPENAI_API_KEY 仍使用示例值，请替换为您的实际 API 密钥
        ) else (
            echo    API Key: ********
        )
    )
) else (
    echo ❌ 未找到 AZURE_OPENAI_API_KEY 配置
)

findstr /C:"AZURE_OPENAI_DEPLOYMENT_NAME=" .env >nul
if %errorlevel% equ 0 (
    echo ✅ 找到 AZURE_OPENAI_DEPLOYMENT_NAME 配置
    for /f "tokens=2 delims==" %%a in ('findstr /C:"AZURE_OPENAI_DEPLOYMENT_NAME=" .env') do (
        echo    部署名称: %%a
    )
) else (
    echo ❌ 未找到 AZURE_OPENAI_DEPLOYMENT_NAME 配置
)

echo.
echo 📋 配置清单:
echo ============================================
echo 1. AZURE_OPENAI_ENDPOINT - 您的 Azure OpenAI 资源端点
echo    示例: https://your-resource-name.openai.azure.com/
echo.
echo 2. AZURE_OPENAI_API_KEY - 您的 Azure OpenAI API 密钥
echo    在 Azure 门户的 "密钥和端点" 部分获取
echo.
echo 3. AZURE_OPENAI_DEPLOYMENT_NAME - GPT-4V 部署名称
echo    示例: gpt-4-vision-preview
echo.
echo 💡 完成配置后，运行以下命令测试:
echo    python check_azure_config.py
echo.
pause