import pyautogui
import random
import time
import os
import subprocess

def open_qq():
    # 尝试通过进程名查找QQ
    try:
        # Windows下查找QQ进程
        subprocess.Popen(['taskkill', '/F', '/IM', 'QQ.exe'])
        time.sleep(2)
    except:
        pass
    
    # 启动QQ
    qq_path = r"D:\Software\QQ\QQ.exe"  # 保持原有路径
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
    # 生成随机数字
    random_code = random.randint(100, 999)
    message = f"代码{random_code}，若请假请忽略此条消息，谢谢。"
    
    # 获取屏幕尺寸
    screen_width, screen_height = pyautogui.size()
    
    # 点击聊天窗口底部中间的输入框
    input_box_x = screen_width // 2  # 屏幕中间
    input_box_y = screen_height - 150  # 距离底部150像素
    pyautogui.click(input_box_x, input_box_y)
    time.sleep(1)
    
    # 模拟键盘输入消息
    pyautogui.typewrite(message)
    time.sleep(1)
    
    # 点击发送按钮（或按回车发送）
    pyautogui.press('enter')
    
    print(f"消息已发送！随机码：{random_code}")

def main():
    print("QQ自动发送消息程序启动...")
    print("请确保：")
    print("1. QQ已经登录")
    print("2. 电脑已连接网络")
    print("3. QQ窗口处于正常大小（不要最小化）")
    print("4. QQ窗口在最前面")
    
    # 要发送消息的QQ号
    target_qq = "2402659629"
    
    # 打开QQ
    if not open_qq():
        return
    
    # 搜索用户
    if not search_user(target_qq):
        return
    
    # 发送消息
    send_message()

if __name__ == "__main__":
    # 设置pyautogui的安全设置
    pyautogui.FAILSAFE = True
    main() 