
import threading
from mouse_and_key import keymouse
from mouse_and_key.alert import alert
from ocr import check_box_detect, object_find, object_template
import datetime as dt
import random as rd
import numpy as np
import time
import copy

class RolePlay:
    def __init__(self, window_name):
        self.window_name = window_name
        self.keymouse = keymouse.KeyMouse(self.window_name)
        self.guaji_frequncy = 10
        self.status = {}
        self.hotel_huihe = [5, 10, 17, 24]
        self.reset_axis = np.array([])
        self.huihe = 999
        self.screen_shot = []
        self.xiaoren4 = False
        self.fight = '未知'
        self.get_handel = True
        self.window_xy = ()
        self.want_hotel = False
        self.last_hotel = 99
        self.axis = []
        self.map = '未知'

    def status_refresh(self):
        axis_old, map_old = copy.deepcopy(self.axis), copy.deepcopy(self.map)
        status = check_box_detect.guaji_check(self.window_name)
        self.huihe = status['huihe']
        self.screen_shot = status['screen_shot']
        self.xiaoren4 = status['xiaoren4']
        self.fight = status['fight']
        self.get_handel = status['get_handel']
        self.window_xy = status['window_xy']
        self.axis = status['axis'] if status['axis'] else self.axis
        self.map = status['map'] if status['axis'] else self.map
        if axis_old != self.axis and self.guaji_frequncy <= 3:  # 如果坐标移动了证明非战斗状态
            self.fight = '非战斗'

    def clearn_screen(self):
        cursor_head, cursor_down = object_find.get_single_taget_pos(self.screen_shot, object_template.npc_talk_template1,
                                                             point_or_box=False, threshold=0.7)
        if cursor_head and cursor_down:
            point = np.array(cursor_head) + (np.array(cursor_down) - np.array(cursor_head)) * 3/4
            cursor_head = self.find_cursor()
            if cursor_head:
                move = point - np.array(cursor_head)
                self.keymouse.mouse_move(move[0], move[1])
                self.keymouse.click_rd(times=rd.randint(3, 11))

    def find_cursor(self):
        cursor_head = np.array([])
        cnt = 0
        while not cursor_head:
            self.screen_shot = check_box_detect.get_img(self.window_name)
            cursor_head, _ = object_find.get_single_taget_pos(self.screen_shot, object_template.mouse_template,
                                                              point_or_box=False, threshold=0.7)
            if not cursor_head:
                self.keymouse.mouse_move(rd.randint(-50, 50), rd.randint(-50, 50))
                cursor_head, _ = object_find.get_single_taget_pos(check_box_detect.get_img(self.window_name), object_template.mouse_template,
                                                                  point_or_box=False, threshold=0.7)
                time.sleep(0.6)
                cnt += 1
            if cnt > 5:
                print('寻找鼠标失败')
                self.cursor_move_back()
                break
        # print(cursor_head)
        return cursor_head

    def cursor_move_back(self):
        self.keymouse.move_abs_rd(self.window_xy[0] + rd.randint(200, 300), self.window_xy[1] + rd.randint(200, 400))

    def guaji(self, huihe = 7):
        """
        1. 四小人检测报警
        2. 回合数检   测补充
        3. 自动酒肆
        4. 血蓝量检测 Todo
        """
        reset = False
        last_huihe = ''
        time1 = dt.datetime.now()
        self.hotel_huihe = [-i for i in range(-30, -5, huihe)]
        self.hotel_huihe.remove(30)
        print('住店回合数：', self.hotel_huihe)
        while True:
            self.status_refresh()
            if 31 >= self.huihe >= 29 and reset:
                print(dt.datetime.now(), ' 回合数已经成功重置')
                reset = False

            elif (self.huihe in self.hotel_huihe or self.huihe < 5) and abs(self.last_hotel - self.huihe) > 2:
                self.want_hotel = True
                self.guaji_frequncy = 1

            if self.xiaoren4:
                alert()

            elif self.huihe <= 2:

                alert()
            if self.huihe <= 5:  # 重置自动战斗次数
                print(dt.datetime.now(), ' 尝试重置回合数...')
                reset_point_x, reset_point_y = object_find.get_single_taget_pos(self.screen_shot, object_template.reset_template, point_or_box=True)
                # print(123, reset_point_x, reset_point_y)
                self.clearn_screen()
                # self.cursor_move_back()
                cur = np.array(self.find_cursor())
                #print(111, self.reset_axis, cur)
                try:
                    move = np.array([reset_point_x, reset_point_y]) - cur
                    self.keymouse.mouse_move(move[0]+rd.randint(-30, 30), move[1]+rd.randint(-30, 30))
                    time.sleep(0.5)
                    cur = np.array(self.find_cursor())
                    move = np.array([reset_point_x, reset_point_y]) - cur
                    self.keymouse.mouse_move(move[0], move[1])
                    self.keymouse.click_rd(which='left', times=1)
                    time.sleep(2)
                    reset_point_x, reset_point_y = object_find.get_single_taget_pos(self.screen_shot,
                                                                                    object_template.reset_template,
                                                                                    point_or_box=True)
                    print('checking', reset_point_x, reset_point_y)
                    if not reset_point_x:
                        print('点成取消了。。。')
                        alert()
                    reset = True
                except TypeError:
                    print('游标出了点小问题，重置ing..')
                self.cursor_move_back()

            if self.want_hotel and self.fight == '非战斗':
                print('尝试住店。。。')
                self.keymouse.key_press_release('F6')
                time.sleep(0.5)
                #screen = self.screen_shot
                for i in range(5):
                    top_left_point, _ = object_find.get_single_taget_pos(check_box_detect.get_img(self.window_name), object_template.hotel_template, point_or_box=False, threshold=0.7)
                    if top_left_point:          
                        # print(top_left_point)
                        top_left_point = np.array([top_left_point[0]+20, top_left_point[1]+5])
                        self.cursor_move_back()
                        cur = np.array(self.find_cursor())
                        if cur.any():
                            move = top_left_point - cur
                            self.keymouse.mouse_move(move[0]+18, move[1]-10)
                            self.keymouse.click_rd(which='left', times=2)
                            top_left_point, _ = object_find.get_single_taget_pos(check_box_detect.get_img(self.window_name), object_template.hotel_template, point_or_box=False, threshold=0.7)
                            if not top_left_point:  # 如果酒店窗口消失那么算完成
                                self.want_hotel = False
                                print(dt.datetime.now(),  '住店已完成')
                                self.last_hotel = self.huihe
                                self.guaji_frequncy = 10
                                break
                    else:
                        self.keymouse.key_press_release('F6')
                        time.sleep(0.5)
                        self.status_refresh()
            elif self.huihe != last_huihe:
                time0 = dt.datetime.now()
                delta = (time0 - time1).seconds

                if delta >= (60 * 10): # 大于12分钟未动报警
                    print(time0.strftime("    %Y-%m-%d, %H:%M:%S"), ' 超时未战斗')
                    alert()
                    time1 = time0
                print(time0.strftime("%Y-%m-%d, %H:%M:%S"), '回合:', self.huihe, self.fight, '位置:', self.map, self.axis
                      , '上次住店：', self.last_hotel, '想住店：', self.want_hotel)
                last_huihe = self.huihe

            else:
                self.clearn_screen()
                time1 = dt.datetime.now()

            time.sleep(self.guaji_frequncy)



    def paoshang(self):
        pass

    def diaoyu(self):
        pass


role = RolePlay('梦幻西游 ONLINE - (无与伦比[兰亭序] - 白米℃[11965514])')
role.guaji(8)
