import tkinter as tk
from tkinter import ttk, messagebox
import json
import schedule
import time
import threading
from datetime import datetime
import sys
import os
from qq_auto_send import send_message, search_user, open_qq

class QQAutoSenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QQ自动发送消息")
        self.root.geometry("600x500")  # 增加窗口高度
        
        # 加载配置
        self.load_config()
        
        # 创建界面
        self.create_widgets()
        
        # 定时任务线程
        self.schedule_thread = None
        self.is_running = False

    def load_config(self):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("错误", "未找到配置文件config.json")
            sys.exit(1)

    def save_config(self):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def create_widgets(self):
        # 创建选项卡
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both', padx=5, pady=5)

        # 主页面
        main_frame = ttk.Frame(notebook)
        notebook.add(main_frame, text='主页面')

        # 用户列表
        user_frame = ttk.LabelFrame(main_frame, text='用户列表')
        user_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 修改用户列表列定义
        self.user_tree = ttk.Treeview(user_frame, columns=('选择', 'QQ号', '名称', '状态'), show='headings')
        self.user_tree.heading('选择', text='选择')
        self.user_tree.heading('QQ号', text='QQ号')
        self.user_tree.heading('名称', text='名称')
        self.user_tree.heading('状态', text='状态')
        self.user_tree.column('选择', width=50, anchor='center')
        self.user_tree.pack(fill='both', expand=True, padx=5, pady=5)

        # 添加复选框
        self.user_tree.bind('<Button-1>', self.on_tree_click)

        # 加载用户列表
        self.refresh_user_list()

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', padx=5, pady=5)

        # 添加按钮
        ttk.Button(button_frame, text='添加用户', command=self.add_user_dialog).pack(side='left', padx=5)
        ttk.Button(button_frame, text='删除用户', command=self.delete_user).pack(side='left', padx=5)
        ttk.Button(button_frame, text='立即发送', command=self.send_now).pack(side='left', padx=5)

        # 消息模板设置
        message_frame = ttk.LabelFrame(main_frame, text='消息模板设置')
        message_frame.pack(fill='x', padx=5, pady=5)

        # 消息模板输入框
        self.message_var = tk.StringVar(value=self.config['message_template'])
        message_entry = ttk.Entry(message_frame, textvariable=self.message_var, width=50)
        message_entry.pack(side='left', padx=5, pady=5, fill='x', expand=True)

        # 保存模板按钮
        ttk.Button(message_frame, text='保存模板', command=self.save_message_template).pack(side='left', padx=5, pady=5)

        # 定时设置框架
        schedule_frame = ttk.LabelFrame(main_frame, text='定时设置')
        schedule_frame.pack(fill='x', padx=5, pady=5)

        # 定时开关
        self.schedule_var = tk.BooleanVar(value=self.config['schedule']['enabled'])
        ttk.Checkbutton(schedule_frame, text='启用定时发送', variable=self.schedule_var,
                        command=self.toggle_schedule).pack(side='left', padx=5)

        # 时间设置
        ttk.Label(schedule_frame, text='时间：').pack(side='left', padx=5)
        self.hour_var = tk.StringVar(value=str(self.config['schedule']['hour']))
        self.minute_var = tk.StringVar(value=str(self.config['schedule']['minute']))
        ttk.Entry(schedule_frame, textvariable=self.hour_var, width=2).pack(side='left')
        ttk.Label(schedule_frame, text=':').pack(side='left')
        ttk.Entry(schedule_frame, textvariable=self.minute_var, width=2).pack(side='left')

        # 状态标签
        self.status_label = ttk.Label(main_frame, text='就绪')
        self.status_label.pack(side='bottom', pady=5)

    def refresh_user_list(self):
        # 清空现有列表
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        # 添加用户
        for user in self.config['users']:
            status = '启用' if user['enabled'] else '禁用'
            self.user_tree.insert('', 'end', values=('☐', user['qq'], user['name'], status))

    def add_user_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title('添加用户')
        dialog.geometry('300x150')

        ttk.Label(dialog, text='QQ号：').pack(pady=5)
        qq_entry = ttk.Entry(dialog)
        qq_entry.pack(pady=5)

        ttk.Label(dialog, text='名称：').pack(pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(pady=5)

        def save():
            qq = qq_entry.get().strip()
            name = name_entry.get().strip()
            if qq and name:
                self.config['users'].append({
                    'qq': qq,
                    'name': name,
                    'enabled': True
                })
                self.save_config()
                self.refresh_user_list()
                dialog.destroy()
            else:
                messagebox.showerror('错误', 'QQ号和名称不能为空')

        ttk.Button(dialog, text='保存', command=save).pack(pady=10)

    def delete_user(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning('警告', '请选择要删除的用户')
            return
        
        if messagebox.askyesno('确认', '确定要删除选中的用户吗？'):
            for item in selected:
                values = self.user_tree.item(item)['values']
                qq = values[1]
                self.config['users'] = [u for u in self.config['users'] if u['qq'] != qq]
            
            self.save_config()
            self.refresh_user_list()

    def send_now(self):
        if not self.config['users']:
            messagebox.showwarning('警告', '没有可发送的用户')
            return

        threading.Thread(target=self.send_to_all_users).start()

    def send_to_all_users(self):
        self.status_label['text'] = '正在发送...'
        
        # 打开QQ
        if not open_qq():
            self.status_label['text'] = 'QQ启动失败'
            return

        # 遍历发送消息
        for item in self.user_tree.get_children():
            values = self.user_tree.item(item)['values']
            if values[0] == '☑':  # 只发送选中的用户
                qq = values[1]
                user = next((u for u in self.config['users'] if u['qq'] == qq), None)
                if user and user['enabled']:
                    try:
                        if search_user(user['qq']):
                            send_message()
                            time.sleep(2)
                    except Exception as e:
                        print(f"发送给{user['qq']}失败: {e}")

        self.status_label['text'] = '发送完成'

    def toggle_schedule(self):
        enabled = self.schedule_var.get()
        self.config['schedule']['enabled'] = enabled
        self.save_config()

        if enabled:
            self.start_schedule()
        else:
            self.stop_schedule()

    def start_schedule(self):
        if self.schedule_thread is None or not self.schedule_thread.is_alive():
            self.is_running = True
            print("定时任务已启动")  # 添加调试信息
            self.schedule_thread = threading.Thread(target=self.schedule_loop)
            self.schedule_thread.daemon = True
            self.schedule_thread.start()

    def stop_schedule(self):
        self.is_running = False
        if self.schedule_thread:
            self.schedule_thread.join()

    def schedule_loop(self):
        schedule.clear()
        
        # 设置定时任务
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())
        print(f"定时任务已设置：每天 {hour:02d}:{minute:02d} 执行")  # 添加调试信息
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(self.send_to_all_users)
        
        while self.is_running:
            print("定时任务运行中...")  # 添加调试信息
            schedule.run_pending()
            time.sleep(30)

    def save_message_template(self):
        new_template = self.message_var.get().strip()
        if not new_template:
            messagebox.showerror('错误', '消息模板不能为空')
            return
        
        if '{code}' not in new_template:
            messagebox.showerror('错误', '消息模板必须包含{code}作为随机码占位符')
            return
        
        self.config['message_template'] = new_template
        self.save_config()
        messagebox.showinfo('成功', '消息模板已保存')

    def on_tree_click(self, event):
        region = self.user_tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.user_tree.identify_column(event.x)
            if column == "#1":  # 第一列是复选框列
                item = self.user_tree.identify_row(event.y)
                current_value = self.user_tree.set(item, '选择')
                new_value = '☑' if current_value != '☑' else '☐'
                self.user_tree.set(item, '选择', new_value)

def main():
    root = tk.Tk()
    app = QQAutoSenderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 