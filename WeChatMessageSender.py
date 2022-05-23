from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import time
import psutil


# 输入进程名，获取PID
def get_pid(p_name):
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p_name in p.name():
            return pid


chat_name = "chat_name"  # 需要发送消息的聊天名称
message = "message"  # 需要发送的消息
we_chat_path = r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe"  # 微信路径

# 获取微信PID并获取微信窗口
we_chat_id = get_pid("WeChat.exe")
app = Application(backend='uia').connect(process=we_chat_id)
we_chat_main_dialog = app.window(class_name='WeChatMainWndForPC')

# 微信挂在后台时，通过再次运行唤醒
if not we_chat_main_dialog.exists():
    tmp = Application().start(we_chat_path)

# 通过先最小化，再恢复使得窗口置顶
we_chat_main_dialog.minimize()
we_chat_main_dialog.restore()

# 通过搜索，定位聊天
search_elem = we_chat_main_dialog.child_window(control_type='Edit', title='搜索')
search_elem.click_input()
search_elem.type_keys('^a').type_keys(chat_name)
time.sleep(1)
send_keys('{ENTER}')

# 点击要发送消息的聊天
chat_list = we_chat_main_dialog.child_window(control_type='List', title='会话')
for chat_item in chat_list.items():
    if chat_name in chat_item.element_info.name:
        chat_item.click_input()
        time.sleep(1)

# 获取聊天记录
message_list = we_chat_main_dialog.child_window(control_type='List', title='消息')
for message_item in message_list.items():
    print(message_item)

# 输入并发送消息
edit_elem = we_chat_main_dialog.child_window(control_type='Edit', title='输入')
edit_elem.type_keys('^a').type_keys(message, with_spaces=True)
time.sleep(1)
send_keys('{ENTER}')
