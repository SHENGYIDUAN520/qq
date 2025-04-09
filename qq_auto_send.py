import pyautogui
import random
import time
import os
import subprocess
import json
import pyperclip

def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

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
    qq_path = config['qq_path']  # 从配置文件读取QQ路径
    if os.path.exists(qq_path):
        subprocess.Popen([qq_path])
    else:
        print("未找到QQ程序，请手动打开QQ")
        return False
    
    # 等待QQ启动
    print("等待QQ启动...")
    time.sleep(10)
    return True

def search_user(qq_number):
    print("开始搜索用户...")
    # 等待QQ窗口完全加载
    time.sleep(2)
    
    try:
        # 查找搜索框图像
        print("正在寻找搜索框...")
        search_box = pyautogui.locateOnScreen('image.png', confidence=0.8)
        if search_box:
            # 点击搜索框中心位置
            center = pyautogui.center(search_box)
            pyautogui.click(center)
            print("找到并点击了搜索框")
        else:
            print("未找到搜索框，请确保QQ窗口在最前面")
            return False
    except Exception as e:
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
    search_result_y = center.y + 100  # 搜索结果在搜索框下方100像素
    pyautogui.click(center.x, search_result_y)
    time.sleep(2)
    return True

def send_message():
    print("准备发送消息...")
    # 从配置文件读取消息模板
    config = load_config()
    message_template = config['message_template']
    
    # 生成3位随机数字（100-999）
    random_code = random.randint(100, 999)
    
    message = message_template.format(code=random_code)
    
    try:
        # 查找输入框图像
        print("正在寻找输入框...")
        input_box = pyautogui.locateOnScreen('copy.png', confidence=0.8)
        if input_box:
            # 点击输入框中心位置
            center = pyautogui.center(input_box)
            pyautogui.click(center)
            print("找到并点击了输入框")
        else:
            print("未找到输入框，使用默认位置点击")
            # 获取屏幕尺寸
            screen_width, screen_height = pyautogui.size()
            # 点击聊天窗口底部中间的输入框
            input_box_x = screen_width // 2  # 屏幕中间
            input_box_y = screen_height - 150  # 距离底部150像素
            pyautogui.click(input_box_x, input_box_y)
    except Exception as e:
        print(f"输入框识别出错: {e}，使用默认位置点击")
        # 获取屏幕尺寸
        screen_width, screen_height = pyautogui.size()
        # 点击聊天窗口底部中间的输入框
        input_box_x = screen_width // 2  # 屏幕中间
        input_box_y = screen_height - 150  # 距离底部150像素
        pyautogui.click(input_box_x, input_box_y)
    
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
    
    # 搜索用户
    if not search_user("2402659629"):
        exit(1)
    
    # 发送消息
    send_message() 