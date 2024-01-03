import basic
import cv2
import time

monkey_position = {"l_t":(56, 293), "l_d":(56, 467), "r_t":(438, 292), "r_d":(437, 466)}
menu_position = {"去试试":(248, 572), "开始战斗":(247, 605), "翻找":(250, 574)}
other_position = {"路牌":(247, 455), "传送门":(445, 647), "箱子":(243, 190)}

handle = basic.get_handle()

def start_fight(handle)->bool:
    while True:
        dts = basic.match_template(handle, cv2.imread('./img/7th/try.png'), match_threshold=0.9)
        if len(dts)>0:
            break
    print("进入场景")
    basic.left_mouse_click(handle=handle, point=menu_position['去试试'])
    time.sleep(3)
    print("开始进攻")
    while True:
        dts = basic.match_template(handle, cv2.imread('./img/7th/sign.png'), match_threshold=0.9)
        if len(dts)>0:
            break
    basic.left_mouse_click(handle=handle, point=other_position['路牌'])
    time.sleep(2)
    while True:
        dts = basic.match_template(handle, cv2.imread('./img/7th/fight.png'), match_threshold=0.9)
        if len(dts)>0:
            break
    basic.left_mouse_click(handle=handle, point=menu_position['开始战斗'])
    print("----------")
    for _ in range(10):
        time.sleep(3)
        print("#", end="", flush=True)
    print("\n战斗结束")

    dts = basic.match_template(handle, cv2.imread('./img/7th/portal.png'), match_threshold=0.9)
    if len(dts)==0:
        print("战斗失败")
        return False
    basic.left_mouse_click(handle=handle, point=other_position['箱子'])
    time.sleep(2)
    basic.left_mouse_click(handle=handle, point=menu_position['翻找'])
    time.sleep(2)
    print("返回")
    basic.left_mouse_click(handle=handle, point=other_position['传送门'])
    time.sleep(5)

    return True


def mumu_record(handle, path):
    resolution_x, resolution_y = handle.right-handle.left, handle.bottom-handle.top
    with open(path, "r", encoding='gb18030', errors='ignore') as f:
        data = f.read()
        actions = eval(data)['actions']

        for ele in actions[1:-1]:
            # print(ele)
            ele_data = ele['data']
            timing = int(ele['timing'])//1000+1
            print(f"休息{timing}秒")
            time.sleep(timing)
            if ele_data!='release':
                point_str = ele_data.split(":")[1][1:-1]
                dx, dy = list(map(float, point_str.split(",")))
                x, y = int(dx*resolution_x), int(dy*resolution_y)
                basic.left_mouse_click(handle, (x, y))
                print(f"点击({x},{y})")


if handle:
    
    # temp_img = cv2.imread('./img/7th/box1.png')
    # dts = basic.match_template(handle, temp_img, match_threshold=0.9)
    # print(dts)
    

    # 买装备
    mumu_record(handle, "./77.mmor")

    for index in range(10):
        print(f"选择猴子,右上第{index}次数")
        basic.left_mouse_click(handle=handle, point=monkey_position['r_t'])
        time.sleep(1)
        start_fight(handle)

    for index in range(10):
        print(f"选择猴子,右下第{index}次数")
        basic.left_mouse_click(handle=handle, point=monkey_position['r_d'])
        time.sleep(1)
        start_fight(handle)
    
    while True:
        print("开始打boss")
        time.sleep(5)
        basic.left_mouse_click(handle=handle, point=other_position["箱子"])
        time.sleep(1.2)
        basic.left_mouse_click(handle=handle, point=menu_position['开始战斗'])
        time.sleep(5)
        basic.left_mouse_click(handle=handle, point=other_position['路牌'])
        time.sleep(2)
        dts = basic.match_template(handle, cv2.imread('./img/7th/pay.png'), match_threshold=0.9)
        basic.left_mouse_click(handle=handle, point=dts[0])
        time.sleep(1)
        dts = basic.match_template(handle, cv2.imread('./img/7th/1.png'), match_threshold=0.9)
        basic.left_mouse_click(handle=handle, point=dts[0])
        time.sleep(1)
        dts = basic.match_template(handle, cv2.imread('./img/7th/sign.png'), match_threshold=0.9)
        basic.left_mouse_click(handle=handle, point=dts[0])
        time.sleep(1)
        print("开始战斗")
        basic.left_mouse_click(handle=handle, point=menu_position['开始战斗'])
        print("----------")
        for _ in range(10):
            time.sleep(3)
            print("#", end="", flush=True)

        dts = basic.match_template(handle, cv2.imread('./img/7th/portal.png'), match_threshold=0.9)
        if len(dts)>0:
            print("通关")
            basic.left_mouse_click(handle=handle, point=dts[0])
            break
        print("战斗失败,重新再打")


    # dts = basic.match_template(handle, cv2.imread('./img/7th/sign.png'), match_threshold=0.9)
    # basic.left_mouse_click(handle=handle, point=dts[0])



    # basic.left_mouse_click(handle=handle, point=(100, 100))
    # pit  = basic.get_screenshot(handle, is_gray=True)

   
    # temp_img = cv2.imread('./template/dark_hide_monster.png')


    # cv2.imshow("1a", img_bottom)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

