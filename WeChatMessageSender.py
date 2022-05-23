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


chat_name = "chat_name"

# 获取微信PID并获取微信窗口
we_chat_id = get_pid("WeChat.exe")
app = Application(backend='uia').connect(process=we_chat_id)
win_main_Dialog = app.window(class_name='WeChatMainWndForPC')

# 通过先最小化，再恢复使得窗口置顶
win_main_Dialog.minimize()
win_main_Dialog.restore()

# 通过搜索，定位聊天
search_elem = win_main_Dialog.child_window(control_type='Edit', title='搜索')
search_elem.click_input()
search_elem.type_keys('^a').type_keys(chat_name)
time.sleep(1)
send_keys('{ENTER}')

chat_list = win_main_Dialog.child_window(control_type='List', title='会话')
for chat_item in chat_list.items():
    if chat_name in chat_item.element_info.name:
        chat_item.click_input()
        time.sleep(1)

message_list = win_main_Dialog.child_window(control_type='List', title='消息')
for message_item in message_list.items():
    print(message_item)

# 输入消息
edit_elem = win_main_Dialog.child_window(control_type='Edit', title='输入')
edit_elem.type_keys('^a').type_keys('预约实验', with_spaces=True)
time.sleep(1)
send_keys('{ENTER}')
