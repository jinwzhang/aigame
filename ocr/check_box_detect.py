import win32api, win32con, win32gui
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import easyocr
from PIL import Image, ImageGrab
import numpy as np
import re
import datetime as dt

ch_ocr_reader = easyocr.Reader(['ch_sim'])


def get_window_pos(name):
    name = name
    handle = win32gui.FindWindow(0, name)
    # 获取窗口句柄
    if handle == 0:
        return None
    else:
        return win32gui.GetWindowRect(handle), handle


def xiaoren4_check(whole_text):
    # 通过OCR文字判断是否出现四小人检测
    check = [whole_text.find('恭喜你'), whole_text.find('本场战斗'), whole_text.find('你将会得到'), whole_text.find('意外奖励'),
             whole_text.find('关闭窗口')]
    check = [1 for i in check if i > -1]
    if sum(check) > 1:
        print(dt.datetime.now(), ' 触发四小人检验')
        return True
    return False


def fight_check(whole_text):
    # 通过OCR文字判断是否正在战斗
    t_check = [whole_text.find('卷王'), whole_text.find('非卷'), whole_text.find('喽啰'),
               whole_text.find('恶鬼'), whole_text.find('帮凶')]
    t_check = [1 for i in t_check if i > -1]
    f_check = [whole_text.find('任务追踪')]
    f_check = [1 for i in f_check if i > -1]
    if sum(t_check) > 0:
        return '战斗'
    if sum(f_check) > 0:
        return '非战斗'
    return '未知'


def get_img(window_name):
    (x1, y1, x2, y2), _ = get_window_pos(window_name)
    img_ready = ImageGrab.grab((x1, y1, x2, y2))
    return np.array(img_ready)


def guaji_check(window_name):
    date = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    status = {'screen_shot': [], 'topleft_axis': (), 'huihe': 999,
              'xiaoren4': False, 'fight': '未知',
              'get_handel': True, 'window_xy': (),
              'axis': [], 'map': '未知'}
    (x1, y1, x2, y2), handle = get_window_pos(window_name)
    status['window_xy'] = np.array([x1, y1])
    status['topleft_axis'] = (x1, y1)
    try:
        win32gui.SetForegroundWindow(handle)  # 把窗口放到顶层
    except Exception as e:
        status['get_handel'] = False

    img_ready = ImageGrab.grab((x1, y1, x2, y2))
    arr = np.array(img_ready)
    status['screen_shot'] = arr

    ocr_text = ch_ocr_reader.readtext(arr)
    whole_text = ';'.join([i[1] for i in ocr_text])   # 合并所有检测到的文字
    status['fight'] = fight_check(whole_text)

    if xiaoren4_check(whole_text):
        img_ready.save(r'.\ocr\IMG\%s.jpg' % date)  # 存储4小人检测图片
        status['xiaoren4'] = True
    buffer = []
    for i in ocr_text:
        text, prob = i[1], i[2]
        loc_left, loc_right = text.find('['), text.find(']')
        if loc_left > -1 and loc_right > -1 and text.find(',') > -1:
            axis = text[loc_left: loc_right+1]
            try:
                axis = eval(axis)
            except:
                pass
            if isinstance(axis, list):
                status['axis'] = axis
                status['map'] = text[:loc_left+1]
                # print(axis, text[:loc_left])
        if prob > 0.5:
            buffer.append(text)
        if text.find('剩余') > -1 and text.find('回合') > -1:
            text = text.replace('|', '1')
            huihe = re.findall(r'\d+', text)
            if huihe:
                huihe = int(''.join(huihe))
            # print(dt.datetime.now(), '剩余回合数：', huihe)
            if isinstance(huihe, int):
                status['huihe'] = huihe
        # if text.find('重置') > -1:  # 取得重置按钮的坐标
        #     rectangle = i[0]
        #     xy = np.array([0, 0])
        #     for i in rectangle:
        #         xy += np.array(i)
        #     xy //= 4
        #     # xy += np.array([x1, y1])
        #     status['reset_loc'] = xy

    # print(buffer)
    return status


if __name__ == '__main__':
    guaji_check('梦幻西游 ONLINE - (无与伦比[兰亭序] - 白米℃[11965514])')

