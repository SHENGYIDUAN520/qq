@echo off
echo ===== QQ自动发送消息系统 - 安装与运行 =====
echo 作者: YI
echo 日期: 2024-04-09
echo.

echo 正在检查Python环境...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo Python未安装，请先安装Python 3.6+
    pause
    exit
)

echo.
echo 正在安装依赖...

echo 1. 尝试安装Pillow (二进制包)...
pip install pillow --only-binary=:all:

echo 2. 安装其他依赖...
pip install pyautogui opencv-python schedule mouse keyboard pyperclip

echo.
echo 依赖安装完成!

echo.
echo 请选择要运行的程序:
echo 1. 图形界面版本 (qq_auto_send_gui.py)
echo 2. 命令行版本 (qq_auto_send.py)
echo 3. 退出

set /p choice="请输入选择 (1-3): "

if "%choice%"=="1" (
    echo 正在启动图形界面版本...
    python qq_auto_send_gui.py
) else if "%choice%"=="2" (
    echo 正在启动命令行版本...
    python qq_auto_send.py
) else if "%choice%"=="3" (
    echo 已退出。
) else (
    echo 无效的选择，已退出。
)

pause 