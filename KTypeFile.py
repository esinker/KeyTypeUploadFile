# -*- coding:utf-8 -*-
import time
from pynput import keyboard
import base64
import logging

# from pykeyboard import PyKeyboard 这个类库也可以实现打字，但是远不如 pynput 放在这里留个备份吧

IS_PAUSE = True
STOP_TYPING = False

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]%(message)s ')


def press_key(key):
    global STOP_TYPING
    if key == keyboard.Key.esc:
        logging.info(f"您按下了ESC键")
        if key == keyboard.Key.esc:
            STOP_TYPING = True
        return False


def release_key(key):
    global IS_PAUSE
    if key == keyboard.Key.pause:
        if not IS_PAUSE:
            IS_PAUSE = True
            logging.info(f"程序暂停运行")
        else:
            IS_PAUSE = False
            logging.info(f"程序继续运行")


def listen_key():
    # 监听键盘不阻塞模式放在后台运行
    listener = keyboard.Listener(
        on_press=press_key,
        on_release=release_key)
    listener.start()


def file2base64(file_path):
    """将文件以二进制转成base64字符串"""
    with open(file_path, 'rb') as f:
        base64_str = base64.b64encode(f.read())  # base64类型
        b4str = base64_str.decode('utf-8')  # str
        return b4str


def b64str2file(base64_str_file, save_file_name):
    """将读取的base64 字符串写入到文件，这个方法一般在目标机器执行"""
    with open(base64_str_file, 'rb') as f:
        base64_str = f.read()
    with open(save_file_name, 'wb') as f:
        f.write(base64.b64decode(base64_str))


def spilt_list(like_list, one_len):
    # 将字符串按照特定长度等分
    for i in range(0, len(like_list), one_len):
        yield like_list[i:i + one_len]


def type_str(in_str,
             *,
             one_step_len=30,
             step_interval=0.2):
    """

    :param in_str: 传入的base64 字符串
    :param one_step_len: 每次要输入多少字符串，切不可太长，不然接收端响应不过来，会卡死
    :param step_interval: 每次输入one_step_len 个字符串后，暂停多长时间，以给ide反应时间
    :return:
    """
    listen_key()
    kb = keyboard.Controller()
    logging.warning("开始切分base64字符串，"
                    "程序书写时请确保将光标移动到要输入的编辑器中,并确保输入法一定是英文状态（大写键关闭）。"
                    "当第一次按下Pause时开始自动书写，"
                    "第二次按下Pause时程序将暂停书写，以此类推。"
                    "当按下Esc时程序退出。")
    global IS_PAUSE, STOP_TYPING
    for i in spilt_list(in_str, one_step_len):
        if STOP_TYPING:
            logging.info("程序中止")
            break
        log_times = 0
        while IS_PAUSE and not STOP_TYPING:
            if log_times == 0:
                logging.info("目前程序是暂停状态按下Pause开始运行，开始运行前请仔细阅读上面文字")
                log_times += 1
            time.sleep(1)
        time.sleep(step_interval)
        kb.type(i)
    logging.info("输入完毕")


def type_file(from_file_path, one_step_len=30, step_interval=0.2):
    logging.info("开始读取文件，并转化成base64字符串")
    b4str = file2base64(from_file_path)
    type_str(b4str, one_step_len=one_step_len, step_interval=step_interval)




if __name__ == '__main__':
    # 调用 type_file 方法传输文件，文件最好压缩下，能节省时间
    src_file_path = 'testfile.zip'
    type_file(src_file_path, one_step_len=30, step_interval=0.2)
    # 调用type_str 方法传输文字
    instr = """test word """
    type_str(instr)
    # 如果远程有python环境可以调用b64str2file方法将BASE64字符串转成文件
    b64str2file("frombase64str.txt", "origfile.zip")

