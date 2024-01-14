import win32con, win32api
import win32gui
import pyautogui

import sys, os
import time

# import pyautogui
import cv2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
import qimage2ndarray

import numpy as np


distance_threshold = 100          # 重复框检测时IOU阈值


class HANDLE():
    def __init__(self, handle_id) -> None:

        self.handle_id = handle_id       # 句柄ID
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(self.handle_id)    # 窗口长宽高



# 获得游戏句柄
def get_handle(FrameTitle = "不思议迷宫"):
    mumu_handle_id = win32gui.FindWindow(0, FrameTitle) | win32gui.FindWindow(FrameTitle, None)
    handle_id = win32gui.FindWindowEx(mumu_handle_id, 0, None, "MuMuPlayer")

    if handle_id is not None:
        return HANDLE(handle_id=handle_id)
    else:
        return None
    
# 获得模拟器句柄
def get_mumu_handle(FrameTitle = "不思议迷宫"):
    mumu_handle_id = win32gui.FindWindow(0, FrameTitle) | win32gui.FindWindow(FrameTitle, None)

    if mumu_handle_id is not None:
        return HANDLE(handle_id=mumu_handle_id)
    else:
        return None


# 调用mumu模拟器的录制文件
def load_mumu_video(handle:HANDLE, path):
    resolution_x, resolution_y = handle.right-handle.left, handle.bottom-handle.top

    # with open(path, "r", encoding='gb18030', errors='ignore') as f:
    with open(path, "r", encoding='utf-8') as f:
        data = f.read()
        actions = eval(data)['actions']

        # 遍历每一次动作
        for ele in actions[1:-1]:
            # print(ele)
            ele_data = ele['data']
            timing = int(ele['timing'])//1000+1
            # print(f"休息{timing}秒")
            time.sleep(timing)
            if ele_data[:9]=='press_rel':

                point_str = ele_data.split(":")[1][1:-1]
                dx, dy = list(map(float, point_str.split(",")))
                x, y = int(dx*resolution_x), int(dy*resolution_y)
                left_mouse_click(handle, (x, y))
                print(f"点击({x},{y})")




# 模拟鼠标左键点击
def left_mouse_click(handle:HANDLE, point:tuple, normalize=False, size=(0, 0))->None:
    if normalize:
        # resolution_x, resolution_y = handle.right-handle.left, handle.bottom-handle.top   # 没有截图之前
        # resolution_x, resolution_y = 519, 923                                             # 截图之后变为图像大小
        size = (handle.right-handle.left, handle.bottom-handle.top)
        new_point = (int(point[0]*size[0]), int(point[1]*size[1]))
    else:
        new_point = point

    # print(new_point)
    position = win32api.MAKELONG(new_point[0], new_point[1])
    win32api.SendMessage(handle.handle_id, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, position)
    win32api.SendMessage(handle.handle_id, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, position)
    return 


# handle-句柄; 获取截图(实时画面截图，以屏幕像素点为准)，可选转灰
def get_screenshot(handle:HANDLE):
    # Qt5截图
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(handle.handle_id).toImage()
    # Qimage转ndarray
    img_z = qimage2ndarray.rgb_view(img)


    img_z = cv2.resize(img_z, (handle.right-handle.left, handle.bottom-handle.top))      # 图片转成100%分辨率大小

    img_z = cv2.cvtColor(img_z, cv2.COLOR_BGR2RGB)  # BGR转RGB
    img_g = cv2.cvtColor(img_z, cv2.COLOR_BGR2GRAY)  # BGR转灰度
    return img_g, img_z   # 返回灰度图，色彩图


#  伪IOU计算，两点之间差10即可   true相距远保留
def ComputeIOU(box1, box2)->bool:
    return True if (box1[0]-box2[0])**2+(box1[1]-box2[1])**2>distance_threshold else False


# 没想到这里也要用到nms...
def nms(dets, h, w):
    dets.sort(key=lambda x:x[2])   # 根据值进行排序
    dets = np.array(dets)
    pick_bboxes = []
    while dets.shape[0]:
        bbox = dets[-1]   # 取最大conf的dt
        keep_index = np.array([ComputeIOU(bbox, box) for box in dets[:-1]]+[False])
        dets = dets[keep_index]    

        pick_bboxes.append((int(bbox[0]+w/2), int(bbox[1]+h/2)))
    
    return pick_bboxes



def match_template(handle:HANDLE, img_template_list, match_threshold=0.8):
    img_bottom, _ = get_screenshot(handle) 

    dts = []
    for img_template in img_template_list:
        # 彩色图转灰度图
        if img_template.ndim ==3:
            img_template = cv2.cvtColor(img_template, cv2.COLOR_BGR2GRAY)

        h, w = img_template.shape[:2]
        # 模板匹配
        match = cv2.matchTemplate(img_bottom, img_template, cv2.TM_CCOEFF_NORMED)

        rows, cols = np.where(match > match_threshold)  # (2, len)  第一行x，第二行y

        for i in range(len(rows)):
            dts.append((cols[i], rows[i], match[rows[i], cols[i]]))

    # 做nms
    nms_dts = nms(dts, h=h, w=w)

    # 调试
    # for ele in nms_dts:
    #     cv2.circle(img_bottom, ele, 10, (0, 0, 255), 4)
    # cv2.imshow("1a", img_bottom)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return nms_dts


def find_and_click(handle:HANDLE, path, sleep_time=1, match_threshold = 0.85):
    while True:
        dts = match_template(handle, [imread(handle, path)], match_threshold=match_threshold)
        if len(dts)>0:
            break
    # print(dts)
    left_mouse_click(handle=handle, point=dts[0])
    time.sleep(sleep_time)


# 截图默认在（1280， 720下截图，读取图片时候做大小变换）, 不然模板匹配的时候会出错
def imread(handle:HANDLE, img_path):
    img = cv2.imread(img_path)
    default_h = 1280
    default_w = 720

    handle_h = handle.bottom-handle.top
    handle_w = handle.right-handle.left

    img = cv2.resize(img, (int(img.shape[1]*handle_w/default_w), int(img.shape[0]*handle_h/default_h)))

    return img


# 坐标转换，将几行几列(从1开始)变成点击坐标(坐标xy颠倒)
def position_trans(handle:HANDLE, pos:tuple)->tuple:
    rows = (0, 305, 430, 555, 680, 805, 930)           # x轴 6行每行中心点坐标   190+i*87
    cols = (0, 85, 225, 365, 505, 645)

    weight = 720
    height = 1280

    handle_h = handle.bottom-handle.top
    handle_w = handle.right-handle.left

    return (int(cols[pos[1]]*handle_w/weight), int(rows[pos[0]]*handle_h/height))


# 小sl
def SL_basic(handle:HANDLE):
    # basic.load_mumu_video(self.handle, "./img/mumu_video/小xl.mmor")
    find_and_click(handle, "./img/common/setting.png", 1)
    find_and_click(handle, "./img/common/account.png", 1)
    find_and_click(handle, "./img/common/logout.png", 8)
    find_and_click(handle, "./img/common/startgame.png", 8)
    find_and_click(handle, "./img/common/SLsure.png", 1)
    find_and_click(handle, "./img/common/adventure.png", 7)
    time.sleep(1)
    while True:
        dts = match_template(handle, [imread(handle, "./img/common/setting.png")], match_threshold=0.9)
        if len(dts)>0:
            break

# 暂离
def save_staute(handle:HANDLE):
    left_mouse_click(handle=handle, point=(0.0847222,0.0351563), normalize=True)   # 点左上角

    find_and_click(handle, "./img/common/leave.png", 5)
    find_and_click(handle, "./img/common/SLsure.png", 1)
    find_and_click(handle, "./img/common/back.png", 7)
    time.sleep(1)
    while True:
        dts = match_template(handle, [imread(handle, "./img/common/setting.png")], match_threshold=0.9)
        if len(dts)>0:
            break

# 执行一次断网，再执行联网
def net_state_change():
    pyautogui.hotkey('win', 'a')
    time.sleep(0.5)
    pyautogui.press('right')
    time.sleep(0.5)
    pyautogui.press('right')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.hotkey('win', 'a')
    time.sleep(0.5)