@echo off
chcp 65001 >nul
echo ============================================================
echo   🎫 一键抢票启动器
echo ============================================================
echo.

REM 检查 Cookie 文件
if not exist "output\browser\damai_cookies.json" (
    echo [1/3] 首次使用，先获取 Cookie...
    echo.
    python skills/browser_controller.py --platform damai --get-cookies
    if errorlevel 1 (
        echo ❌ 获取 Cookie 失败
        pause
        exit /b 1
    )
)

echo [1/3] Cookie 已就绪
echo.

REM 输入票务信息
echo [2/3] 请输入票务信息：
echo.
set /p SESSION=场次 ID: 
set /p SKU=票档 SKU ID: 
set /p BUYER_NAME=购买人姓名：
set /p BUYER_PHONE=购买人手机号：
set /p BUYER_ID=身份证号（可选）: 

echo.
echo [3/3] 开始抢票...
echo.

REM 运行抢票脚本
python skills/ticket_snatcher.py ^
  --platform damai ^
  --session %SESSION% ^
  --sku %SKU% ^
  --buyer-name "%BUYER_NAME%" ^
  --buyer-phone "%BUYER_PHONE%" ^
  --buyer-id "%BUYER_ID%" ^
  --cookies @output\browser\damai_cookies.json ^
  --interval 1 ^
  --max-attempts 200 ^
  --webhook "%FEISHU_WEBHOOK%"

if errorlevel 1 (
    echo.
    echo ❌ 抢票失败
) else (
    echo.
    echo ✅ 抢票成功！
)

echo.
echo ============================================================
pause
