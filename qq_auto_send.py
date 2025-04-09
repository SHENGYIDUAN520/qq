import pyautogui
import random
import time
import os
import sys  # Import sys
import subprocess
import json
import pyperclip

# Helper function to get the correct path for data files
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Get paths to resources
CONFIG_PATH = resource_path('config.json')
IMAGE_SEARCH_PATH = resource_path('image.png')
IMAGE_COPY_PATH = resource_path('image copy.png') # Use correct filename

def load_config():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found at {CONFIG_PATH}")
        return None # Return None if config not found
    except json.JSONDecodeError:
        print(f"Error: Config file at {CONFIG_PATH} is not valid JSON.")
        return None
    except Exception as e:
        print(f"Error loading config file: {e}")
        return None

def open_qq():
    # 尝试通过进程名查找QQ
    try:
        # Windows下查找QQ进程
        subprocess.Popen(['taskkill', '/F', '/IM', 'QQ.exe'])
        time.sleep(2)
    except:
        pass
    
    # 启动QQ
    config = load_config()
    if config is None:
        print("无法加载配置，无法启动QQ")
        return False
        
    qq_path = config.get('qq_path') # Use .get() for safer access
    if not qq_path:
        print("错误：配置文件中未找到 'qq_path'")
        return False
        
    if os.path.exists(qq_path):
        try:
            subprocess.Popen([qq_path])
        except Exception as e:
            print(f"启动QQ时出错 ({qq_path}): {e}")
            return False
    else:
        print(f"错误：未找到QQ程序，请检查路径配置: {qq_path}")
        return False
    
    # 等待QQ启动
    print("等待QQ启动...")
    time.sleep(10) # Consider making this configurable or smarter
    return True

def search_user(qq_number):
    print("开始搜索用户...")
    # 等待QQ窗口完全加载
    time.sleep(2)
    
    try:
        # 查找搜索框图像
        print(f"正在寻找搜索框图像: {IMAGE_SEARCH_PATH}")
        search_box = pyautogui.locateOnScreen(IMAGE_SEARCH_PATH, confidence=0.8)
        if search_box:
            # 点击搜索框中心位置
            center = pyautogui.center(search_box)
            pyautogui.click(center)
            print("找到并点击了搜索框")
        else:
            print("未找到搜索框，请确保QQ窗口在最前面且图像文件存在")
            return False
    except Exception as e:
        # More specific error for pyautogui image not found
        if isinstance(e, pyautogui.ImageNotFoundException):
             print(f"错误: 无法在屏幕上找到搜索框图像 '{os.path.basename(IMAGE_SEARCH_PATH)}'. 请确保图片文件正确且QQ界面可见。")
        else:
            print(f"搜索框识别出错: {e}")
        return False
    
    time.sleep(1)
    
    # 输入QQ号
    pyautogui.typewrite(str(qq_number))
    time.sleep(2)
    
    # 按下回车键搜索
    pyautogui.press('enter')
    time.sleep(2)
    
    # 点击第一个搜索结果（在搜索框下方约100像素处）
    # Need to check if 'center' was actually assigned
    if 'center' in locals():
        search_result_y = center.y + 100  # 搜索结果在搜索框下方100像素
        pyautogui.click(center.x, search_result_y)
        time.sleep(2)
        return True
    else:
        # This case should ideally not happen if search_box was found
        print("错误：无法确定搜索框位置来点击结果。")
        return False

def send_message():
    print("准备发送消息...")
    # 从配置文件读取消息模板
    config = load_config()
    if config is None:
        print("无法加载配置，无法发送消息")
        return # Return instead of proceeding
        
    message_template = config.get('message_template')
    if not message_template:
        print("错误：配置文件中未找到 'message_template'")
        return
    
    # 生成3位随机数字（100-999）
    random_code = random.randint(100, 999)
    
    message = message_template.format(code=random_code)
    
    try:
        # 查找输入框图像
        print(f"正在寻找输入框图像: {IMAGE_COPY_PATH}")
        input_box = pyautogui.locateOnScreen(IMAGE_COPY_PATH, confidence=0.8)
        if input_box:
            # 点击输入框中心位置
            center = pyautogui.center(input_box)
            pyautogui.click(center)
            print("找到并点击了输入框")
        else:
            print("未找到输入框图像，将尝试点击屏幕默认位置")
            # 获取屏幕尺寸
            screen_width, screen_height = pyautogui.size()
            # 点击聊天窗口底部中间的输入框 (Adjust if needed)
            input_box_x = screen_width // 2
            input_box_y = screen_height - 150
            pyautogui.click(input_box_x, input_box_y)
    except Exception as e:
        if isinstance(e, pyautogui.ImageNotFoundException):
             print(f"错误: 无法在屏幕上找到输入框图像 '{os.path.basename(IMAGE_COPY_PATH)}'. 将尝试点击屏幕默认位置。")
        else:
            print(f"输入框识别出错: {e}，将尝试点击屏幕默认位置")
        # Fallback to clicking default position
        try:
            screen_width, screen_height = pyautogui.size()
            input_box_x = screen_width // 2
            input_box_y = screen_height - 150
            pyautogui.click(input_box_x, input_box_y)
        except Exception as click_e:
            print(f"尝试点击默认位置时也出错: {click_e}")
            return # Cannot proceed if clicking fails
    
    time.sleep(1)
    
    # 使用pyperclip复制消息到剪贴板
    pyperclip.copy(message)
    time.sleep(1)
    
    # 粘贴消息
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    
    # 点击发送按钮（或按回车发送）
    pyautogui.press('enter')
    
    print(f"消息已发送！随机码：{random_code}")

if __name__ == "__main__":
    # 设置pyautogui的安全设置
    pyautogui.FAILSAFE = True
    
    # 打开QQ
    if not open_qq():
        exit(1)
    
    # 搜索用户 (Example QQ)
    example_qq = "2402659629" 
    if not search_user(example_qq):
        print(f"搜索用户 {example_qq} 失败")
        exit(1)
    
    # 发送消息
    send_message() 