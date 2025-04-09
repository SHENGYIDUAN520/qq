# QQ自动发送消息系统

![版本](https://img.shields.io/badge/版本-2.0-blue)
![Python](https://img.shields.io/badge/Python-3.6+-brightgreen)
![tkinter](https://img.shields.io/badge/tkinter-8.6+-yellow)

一个基于Python开发的QQ自动发送消息工具，可以帮助你定时或批量向指定QQ好友发送消息。通过图像识别技术，实现了全自动的消息发送流程。

## 功能特点

- **界面美观**: 使用现代化的clam主题，自定义样式，界面清晰直观
- **自动发送**: 可以设置定时任务，每天自动发送消息
- **批量处理**: 支持向多个QQ好友发送相同内容的消息
- **用户管理**: 方便地添加、删除、启用和禁用用户
- **图像识别**: 使用图像识别技术自动定位QQ搜索框和输入框
- **随机码**: 每条消息中自动生成随机验证码，支持自定义消息模板
- **状态反馈**: 实时显示发送进度和结果统计

## 安装要求

### 环境要求
- Python 3.6+
- Windows操作系统
- QQ客户端

### 安装依赖库
```bash
pip install pyautogui pillow opencv-python pyperclip schedule
```

### 准备工作
1. 确保QQ已安装并能正常登录
2. 准备图像识别需要的图片文件:
   - `image.png` (QQ搜索框图像)
   - `copy.png` (QQ输入框图像)
3. 创建或修改配置文件 `config.json`

## 使用方法

### 基本步骤

1. 启动程序
```bash
python qq_auto_send_gui.py
```

2. 添加用户
   - 点击"添加用户"按钮
   - 输入QQ号和用户名称
   - 选择是否启用该用户
   - 点击"保存"按钮

3. 设置消息模板
   - 在消息模板输入框中编辑消息内容
   - 使用`{code}`占位符表示随机验证码位置
   - 点击"保存模板"按钮

4. 发送消息
   - 立即发送: 点击"立即发送"按钮
   - 定时发送: 设置时间并启用定时发送

### 用户管理

- **添加用户**: 点击"添加用户"，填写信息后保存
- **删除用户**: 选中用户，点击"删除用户"按钮
- **修改状态**: 双击用户列表中的用户可切换启用/禁用状态
- **批量操作**: 选中多个用户，点击"启用选中"或"禁用选中"按钮

### 功能设置

- **定时设置**: 设置每天自动发送的时间，并启用定时发送
- **消息模板**: 设置发送的消息内容，{code}会被替换为100-999之间的随机数字

## 配置文件说明

程序使用`config.json`文件保存配置信息，格式如下：

```json
{
    "qq_path": "D:\\Software\\QQ\\QQ.exe",  // QQ程序路径
    "users": [  // 用户列表
        {
            "qq": "123456789",  // QQ号
            "name": "用户名",    // 用户名称
            "enabled": true     // 是否启用
        }
    ],
    "schedule": {  // 定时设置
        "enabled": true,  // 是否启用定时
        "hour": 8,        // 小时(24小时制)
        "minute": 30      // 分钟
    },
    "message_template": "代码{code}，若请假请忽略此条消息，感谢配合。"  // 消息模板
}
```

## 注意事项

1. **运行环境**
   - QQ必须处于登录状态
   - 运行程序时请勿遮挡QQ窗口
   - 发送消息过程中请勿移动鼠标或操作键盘

2. **图像识别**
   - 确保`image.png`和`copy.png`与程序在同一目录
   - 图像识别可能受屏幕分辨率、主题等因素影响
   - 如识别失败，会尝试使用默认坐标

3. **使用限制**
   - 不要将此程序用于骚扰或违法用途
   - 过于频繁的消息发送可能导致QQ账号被限制

## 版本历史

查看[开发进度.md](开发进度.md)获取详细的版本更新历史。

## 证书

本项目基于MIT许可证开源 