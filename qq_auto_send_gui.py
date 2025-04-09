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
        self.root.geometry("800x800")  # 增加窗口尺寸
        
        # 设置主题样式
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 使用clam主题，更现代化
        
        # 配置样式
        self.configure_styles()
        
        # 加载配置
        self.load_config()
        
        # 创建界面
        self.create_widgets()
        
        # 定时任务线程
        self.schedule_thread = None
        self.is_running = False
        
        # 默认启动定时任务
        self.schedule_var.set(True)  # 设置复选框为选中状态
        self.config['schedule']['enabled'] = True  # 修改配置
        self.save_config()  # 保存配置
        self.start_schedule()  # 启动定时任务
        print("程序启动时已自动开启定时任务")

    def configure_styles(self):
        # 配置Treeview样式
        self.style.configure("Treeview", 
                            background="#F5F5F5",
                            foreground="black",
                            rowheight=25,
                            fieldbackground="#F5F5F5")
        self.style.map("Treeview",
                    background=[('selected', '#4A6984')])
        
        # 配置标题样式
        self.style.configure("Treeview.Heading", 
                            font=('微软雅黑', 10, 'bold'),
                            background="#E1E1E1",
                            foreground="black")
        
        # 配置按钮样式
        self.style.configure("TButton", 
                            font=('微软雅黑', 9),
                            background="#4A6984",
                            foreground="black",
                            padding=6)
        self.style.map("TButton",
                    background=[('active', '#5A7994')])
        
        # 配置标签框样式
        self.style.configure("TLabelframe", 
                            background="#F0F0F0",
                            foreground="#333333")
        self.style.configure("TLabelframe.Label", 
                            font=('微软雅黑', 9, 'bold'),
                            background="#F0F0F0",
                            foreground="#333333")
        
        # 配置标签样式
        self.style.configure("TLabel", 
                            font=('微软雅黑', 9),
                            background="#F0F0F0",
                            foreground="#333333")
        
        # 配置输入框样式
        self.style.configure("TEntry", 
                            font=('微软雅黑', 9),
                            background="white",
                            foreground="black")
        
        # 状态标签特殊样式
        self.style.configure("Status.TLabel", 
                            font=('微软雅黑', 9, 'bold'),
                            foreground="#4A6984")
        
        # 配置Checkbutton样式
        self.style.configure("TCheckbutton", 
                            background="#F0F0F0",
                            font=('微软雅黑', 9))

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
        # 主容器使用Padding
        main_container = ttk.Frame(self.root, padding="10 10 10 10")
        main_container.pack(fill='both', expand=True)
        
        # 创建应用标题
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill='x', pady=(0, 15))
        
        title_label = ttk.Label(title_frame, text="QQ自动发送消息系统", 
                               font=('微软雅黑', 16, 'bold'),
                               foreground="#4A6984")
        title_label.pack(side='left', padx=5)
        
        # 当前时间
        self.time_label = ttk.Label(title_frame, text=self.get_current_time(),
                                  font=('微软雅黑', 10),
                                  foreground="#666666")
        self.time_label.pack(side='right', padx=5)
        self.update_time()
        
        # 创建选项卡
        notebook = ttk.Notebook(main_container)
        notebook.pack(expand=True, fill='both')

        # 主页面
        main_frame = ttk.Frame(notebook, padding="10 10 10 10")
        notebook.add(main_frame, text='主页面')
        
        # 设置页面
        settings_frame = ttk.Frame(notebook, padding="10 10 10 10")
        notebook.add(settings_frame, text='设置')

        # 用户列表 - 主页面
        user_frame = ttk.LabelFrame(main_frame, text='用户列表', padding="8 8 8 8")
        user_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 创建用户列表
        tree_frame = ttk.Frame(user_frame)
        tree_frame.pack(fill='both', expand=True)
        
        self.user_tree = ttk.Treeview(tree_frame, columns=('QQ号', '名称', '状态'), show='headings', height=12)
        self.user_tree.heading('QQ号', text='QQ号')
        self.user_tree.heading('名称', text='名称')
        self.user_tree.heading('状态', text='状态')
        self.user_tree.column('QQ号', width=150, anchor='center')
        self.user_tree.column('名称', width=150, anchor='center')
        self.user_tree.column('状态', width=80, anchor='center')
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.user_tree.pack(side='left', fill='both', expand=True)
        
        # 双击切换状态
        self.user_tree.bind("<Double-1>", self.toggle_selected_user)

        # 按钮框架 - 用户操作
        button_frame = ttk.Frame(user_frame)
        button_frame.pack(fill='x', pady=(8, 0))

        # 添加按钮 - 使用grid布局
        ttk.Button(button_frame, text='添加用户', command=self.add_user_dialog, width=12).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text='删除用户', command=self.delete_user, width=12).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text='启用选中', command=lambda: self.toggle_user_status(True), width=12).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text='禁用选中', command=lambda: self.toggle_user_status(False), width=12).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(button_frame, text='立即发送', command=self.send_now, width=12).grid(row=0, column=4, padx=5, pady=5)

        # 发送设置 - 主页面下方
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill='x', pady=(15, 5))
        
        # 左侧 - 定时设置
        schedule_frame = ttk.LabelFrame(control_frame, text='定时设置', padding="8 8 8 8")
        schedule_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # 定时开关
        schedule_control = ttk.Frame(schedule_frame)
        schedule_control.pack(fill='x', pady=5)
        
        self.schedule_var = tk.BooleanVar(value=self.config['schedule']['enabled'])
        ttk.Checkbutton(schedule_control, text='启用定时发送', variable=self.schedule_var,
                        command=self.toggle_schedule).pack(side='left', padx=5)

        # 时间设置
        time_frame = ttk.Frame(schedule_frame)
        time_frame.pack(fill='x', pady=5)
        
        ttk.Label(time_frame, text='设定时间：').pack(side='left', padx=5)
        
        time_input = ttk.Frame(time_frame)
        time_input.pack(side='left')
        
        self.hour_var = tk.StringVar(value=str(self.config['schedule']['hour']))
        hour_entry = ttk.Entry(time_input, textvariable=self.hour_var, width=3, justify='center')
        hour_entry.pack(side='left')
        
        ttk.Label(time_input, text=':').pack(side='left')
        
        self.minute_var = tk.StringVar(value=str(self.config['schedule']['minute']))
        minute_entry = ttk.Entry(time_input, textvariable=self.minute_var, width=3, justify='center')
        minute_entry.pack(side='left')
        
        ttk.Label(time_frame, text='(24小时制)').pack(side='left', padx=5)

        # 右侧 - 消息模板设置
        message_frame = ttk.LabelFrame(control_frame, text='消息模板设置', padding="8 8 8 8")
        message_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        # 消息模板说明
        ttk.Label(message_frame, text='使用{code}作为随机码占位符：').pack(anchor='w', padx=5, pady=(0, 5))
        
        # 消息模板输入框和保存按钮
        template_frame = ttk.Frame(message_frame)
        template_frame.pack(fill='x')
        
        self.message_var = tk.StringVar(value=self.config['message_template'])
        message_entry = ttk.Entry(template_frame, textvariable=self.message_var, width=50)
        message_entry.pack(side='left', fill='x', expand=True, padx=5)

        # 保存模板按钮
        ttk.Button(template_frame, text='保存模板', command=self.save_message_template, width=10).pack(side='right', padx=5)

        # 设置页面内容
        self.create_settings_page(settings_frame)

        # 底部状态栏
        status_frame = ttk.Frame(main_container, relief='sunken', padding="5 5 5 5")
        status_frame.pack(fill='x', side='bottom', pady=(10, 0))

        self.status_label = ttk.Label(status_frame, text='系统就绪', style="Status.TLabel")
        self.status_label.pack(side='left')
        
        # 版本信息
        version_label = ttk.Label(status_frame, text='v2.0', foreground='#999999')
        version_label.pack(side='right')
        
        # 在创建完所有界面元素后再刷新用户列表
        self.refresh_user_list()

    def create_settings_page(self, parent):
        # 程序设置
        app_settings = ttk.LabelFrame(parent, text='程序设置', padding="8 8 8 8")
        app_settings.pack(fill='x', pady=(0, 10))
        
        # 自动启动设置
        autostart_frame = ttk.Frame(app_settings)
        autostart_frame.pack(fill='x', pady=5)
        
        autostart_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(autostart_frame, text='程序启动时自动开启定时任务', 
                      variable=autostart_var).pack(side='left', padx=5)
        
        # 帮助信息
        help_frame = ttk.LabelFrame(parent, text='使用帮助', padding="8 8 8 8")
        help_frame.pack(fill='both', expand=True)
        
        help_text = """
1. 添加用户：点击"添加用户"按钮，输入QQ号和名称
2. 删除用户：选中用户后点击"删除用户"按钮
3. 修改状态：双击用户可切换启用/禁用状态
4. 发送消息：点击"立即发送"按钮
5. 定时设置：设置每天发送的时间，并启用定时发送
6. 消息模板：设置发送的消息内容，{code}会被替换为随机数字

注意事项：
- 确保QQ已登录且窗口可见
- 发送过程中请勿操作鼠标和键盘
- QQ号请确保正确，否则可能无法找到用户
        """
        help_label = ttk.Label(help_frame, text=help_text, justify='left', wraplength=650)
        help_label.pack(padx=5, pady=5, fill='both', expand=True)

    def update_time(self):
        # 更新时间显示
        self.time_label.config(text=self.get_current_time())
        self.root.after(1000, self.update_time)
        
    def get_current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def toggle_selected_user(self, event):
        """双击切换用户状态"""
        region = self.user_tree.identify("region", event.x, event.y)
        if region == "cell":
            item = self.user_tree.identify_row(event.y)
            if item:
                values = self.user_tree.item(item)['values']
                if values:
                    qq = values[0]  # QQ号在第一列
                    status = values[2]  # 状态在第三列
                    
                    # 切换状态
                    new_status = False if status == '启用' else True
                    
                    # 更新内存中的配置
                    found = False
                    for user in self.config['users']:
                        if str(user['qq']) == str(qq):
                            user['enabled'] = new_status
                            found = True
                            break
                    
                    if found:
                        # 保存配置到文件
                        self.save_config()
                        # 刷新用户列表
                        self.refresh_user_list()
                        messagebox.showinfo('成功', f'用户 {qq} 状态已切换为 {"启用" if new_status else "禁用"}')

    def toggle_user_status(self, enable):
        """切换用户状态按钮功能"""
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning('警告', '请选择要操作的用户')
            return
        
        changed = False
        for item in selected:
            values = self.user_tree.item(item)['values']
            qq = values[0]  # QQ号在第一列
            
            # 更新内存中的配置
            for user in self.config['users']:
                if str(user['qq']) == str(qq):
                    if user['enabled'] != enable:
                        user['enabled'] = enable
                        changed = True
                    break
        
        if changed:
            # 保存配置到文件
            self.save_config()
            # 刷新用户列表
            self.refresh_user_list()
            status_text = '启用' if enable else '禁用'
            messagebox.showinfo('成功', f'已将选中用户设置为{status_text}')

    def refresh_user_list(self):
        """刷新用户列表"""
        # 清空现有列表
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        # 添加用户
        for user in self.config['users']:
            status = '启用' if user['enabled'] else '禁用'
            self.user_tree.insert('', 'end', values=(user['qq'], user['name'], status))
            
        # 更新状态栏
        self.status_label.config(text=f'共 {len(self.config["users"])} 个用户，{sum(1 for u in self.config["users"] if u["enabled"])} 个已启用')

    def add_user_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title('添加用户')
        dialog.geometry('320x230')
        dialog.resizable(False, False)
        dialog.configure(background='#F0F0F0')
        
        # 设置模态对话框
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中对话框
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # 添加内容框架
        content_frame = ttk.Frame(dialog, padding="20 20 20 20")
        content_frame.pack(fill='both', expand=True)

        # 标题
        ttk.Label(content_frame, text='添加新用户', 
                font=('微软雅黑', 12, 'bold'),
                foreground="#4A6984").pack(pady=(0, 15))

        # QQ号输入
        qq_frame = ttk.Frame(content_frame)
        qq_frame.pack(fill='x', pady=5)
        ttk.Label(qq_frame, text='QQ号：', width=8).pack(side='left')
        qq_entry = ttk.Entry(qq_frame)
        qq_entry.pack(side='left', fill='x', expand=True)
        
        # 名称输入
        name_frame = ttk.Frame(content_frame)
        name_frame.pack(fill='x', pady=5)
        ttk.Label(name_frame, text='名称：', width=8).pack(side='left')
        name_entry = ttk.Entry(name_frame)
        name_entry.pack(side='left', fill='x', expand=True)
        
        # 启用状态复选框
        enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(content_frame, text='启用', variable=enabled_var).pack(pady=10)

        # 按钮框架
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill='x', pady=(15, 0))
        
        def save():
            qq = qq_entry.get().strip()
            name = name_entry.get().strip()
            if qq and name:
                # 检查是否已存在相同QQ号的用户
                for user in self.config['users']:
                    if user['qq'] == qq:
                        messagebox.showerror('错误', f'QQ号 {qq} 已存在')
                        return
                        
                self.config['users'].append({
                    'qq': qq,
                    'name': name,
                    'enabled': enabled_var.get()
                })
                self.save_config()
                self.refresh_user_list()
                dialog.destroy()
            else:
                messagebox.showerror('错误', 'QQ号和名称不能为空')

        ttk.Button(button_frame, text='保存', command=save, width=10).pack(side='right', padx=5)
        ttk.Button(button_frame, text='取消', command=dialog.destroy, width=10).pack(side='right', padx=5)

    def delete_user(self):
        """删除选中的用户"""
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning('警告', '请选择要删除的用户')
            return
        
        if messagebox.askyesno('确认', f'确定要删除选中的 {len(selected)} 个用户吗？'):
            deleted_count = 0
            for item in selected:
                values = self.user_tree.item(item)['values']
                if values and len(values) >= 1:
                    qq = str(values[0])  # QQ号在第一列
                    
                    # 创建新的用户列表，排除要删除的QQ号
                    new_users = []
                    for user in self.config['users']:
                        if str(user['qq']) != qq:
                            new_users.append(user)
                    
                    # 检查是否真的删除了用户
                    if len(new_users) < len(self.config['users']):
                        self.config['users'] = new_users
                        deleted_count += 1
            
            # 只有在确实删除了用户的情况下才保存配置
            if deleted_count > 0:
                self.save_config()
                self.refresh_user_list()
                messagebox.showinfo('成功', f'已删除 {deleted_count} 个用户')
            else:
                messagebox.showwarning('警告', '没有用户被删除')

    def send_now(self):
        if not self.config['users']:
            messagebox.showwarning('警告', '没有可发送的用户')
            return
            
        enabled_users = [u for u in self.config['users'] if u['enabled']]
        if not enabled_users:
            messagebox.showwarning('警告', '没有已启用的用户')
            return

        if messagebox.askyesno('确认', f'即将向 {len(enabled_users)} 个启用的用户发送消息，是否继续？'):
            threading.Thread(target=self.send_to_all_users).start()

    def send_to_all_users(self):
        self.status_label.config(text='正在发送消息...')
        
        # 打开QQ
        if not open_qq():
            self.status_label.config(text='QQ启动失败')
            messagebox.showerror('错误', 'QQ启动失败，请检查QQ路径或手动启动QQ')
            return

        # 获取已启用的用户
        enabled_users = [u for u in self.config['users'] if u['enabled']]
        total = len(enabled_users)
        success = 0
        failed = 0

        # 遍历发送消息
        for index, user in enumerate(enabled_users):
            try:
                self.status_label.config(text=f'正在发送 ({index+1}/{total}): {user["name"]}')
                self.root.update()
                
                if search_user(user['qq']):
                    send_message()
                    success += 1
                    time.sleep(2)
                else:
                    failed += 1
            except Exception as e:
                print(f"发送给{user['qq']}失败: {e}")
                failed += 1

        self.status_label.config(text=f'发送完成: 成功 {success} 个, 失败 {failed} 个')
        messagebox.showinfo('发送结果', f'发送完成\n成功: {success} 个\n失败: {failed} 个')

    def toggle_schedule(self):
        enabled = self.schedule_var.get()
        self.config['schedule']['enabled'] = enabled
        self.save_config()

        if enabled:
            self.start_schedule()
            self.status_label.config(text=f'已启用定时发送: {self.hour_var.get()}:{self.minute_var.get()}')
        else:
            self.stop_schedule()
            self.status_label.config(text='已禁用定时发送')

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
            self.schedule_thread.join(timeout=1.0)

    def schedule_loop(self):
        schedule.clear()
        
        # 设置定时任务
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())
        print(f"定时任务已设置：每天 {hour:02d}:{minute:02d} 执行")  # 添加调试信息
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(self.send_to_all_users)
        
        while self.is_running:
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
        self.status_label.config(text='消息模板已更新')

def main():
    root = tk.Tk()
    root.configure(background='#F0F0F0')
    app = QQAutoSenderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()