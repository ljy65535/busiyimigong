import basic
import cv2
import time
import numpy as np
import paddlehub as hub
import difflib
import copy


# 使用地震术
def use_quake(handle):
    time.sleep(0.5)
    print("点击右下角", end=' ', flush=True)
    basic.left_mouse_click(handle=handle, point=(0.854167,0.939063), normalize=True)
    time.sleep(1)
    print("点击卷轴系列", end=' ', flush=True)
    basic.left_mouse_click(handle=handle, point=(0.25,0.782031), normalize=True)
    time.sleep(1)
    print("点击土系魔法", end=' ', flush=True)
    basic.left_mouse_click(handle=handle, point=(0.901389,0.429688), normalize=True)
    time.sleep(1)
    print("点击地震术", end=' ', flush=True)
    basic.left_mouse_click(handle=handle, point=(0.609722,0.36875), normalize=True)
    time.sleep(1)
    print("点击头像使用", end=' ', flush=True)
    basic.left_mouse_click(handle=handle, point=(0.498611,0.947656), normalize=True)
    time.sleep(1)


# 使用死亡波纹
def use_death_ripper(handle):
    time.sleep(0.5)
    print("点击右下角", end=' ', flush=True)
    basic.left_mouse_click(handle=handle, point=(0.854167,0.939063), normalize=True)
    time.sleep(1)
    print("点击卷轴系列", end=' ', flush=True)
    basic.left_mouse_click(handle=handle, point=(0.25,0.782031), normalize=True)
    time.sleep(1)
    print("点击暗系魔法", end=' ', flush=True)
    basic.left_mouse_click(handle=handle, point=(0.888889,0.673438), normalize=True)
    time.sleep(1)
    print("点击死亡波纹", end=' ', flush=True)
    basic.left_mouse_click(handle=handle, point=(0.609722,0.36875), normalize=True)
    time.sleep(1)
    print("点击头像使用", end=' ', flush=True)
    basic.left_mouse_click(handle=handle, point=(0.498611,0.947656), normalize=True)
    time.sleep(1)


# 检测目前已经有的装备，返回列表中缺少的装备  equip_list包含装备路径
def check_equipment(handle:basic.HANDLE, equip_list:list):
    equip_list_copy = copy.deepcopy(equip_list)

    basic.find_and_click(handle, "./img/common/equip_pack.png", 1)   # 点击背包

    # 翻到第一页
    while True:
        left_botton_dts = basic.match_template(handle, [basic.imread(handle, "./img/common/left_bottom.png")], match_threshold=0.85)
        if len(left_botton_dts)>0:
            basic.left_mouse_click(handle=handle, point=left_botton_dts[0])
            time.sleep(0.5)
        else:
            break
    
    # 从第一页依次找
    while True:
        # 所有装备都存在
        if len(equip_list_copy)==0:
            basic.find_and_click(handle, "./img/shenduan/back.png", 1)
            return []
        
        # 查找当前页面装备
        _, img = basic.get_screenshot(handle)

        remove_list = []
        for equip in equip_list_copy:
            equip_dts = basic.match_template(handle, [basic.imread(handle, equip)], match_threshold=0.85)
            if len(equip_dts)>0:
                remove_list.append(equip)
        
        for ele in remove_list:
            equip_list_copy.remove(ele)

        # 翻页
        right_botton_dts = basic.match_template(handle, [basic.imread(handle, "./img/common/right_bottom.png")], match_threshold=0.85)
        if len(right_botton_dts)>0:
            basic.left_mouse_click(handle=handle, point=right_botton_dts[0])
            time.sleep(0.5)
        else:
            break
    
    basic.find_and_click(handle, "./img/shenduan/back.png", 1)
    return equip_list_copy


# 获得装备名字
def obtain_equip_name(handle:basic.HANDLE)->list:
    area = ((0.741667,0.853906), (0.966667,0.908594))  

    print("开始截图并检测")
    screenshot_list = []
    for _ in range(20):
        _, img = basic.get_screenshot(handle)
        h, w, _ = img.shape
        top, down, left, right = int(area[0][1]*h), int(area[1][1]*h), int(area[0][0]*w), int(area[1][0]*w)
        area_img = img[top:down, left:right, :]
        screenshot_list.append(area_img)
        time.sleep(0.1)

    result_list = ocr.recognize_text(images=screenshot_list)
    result_set = set()

    for result in result_list:
        if len(result['data'])==0:
            continue
        det_texts = result['data'][0]['text']
        result_set.add(det_texts)

    return list(result_set)
    

if __name__ == "__main__":  
    ocr = hub.Module(name="ch_pp-ocrv3", enable_mkldnn=True)       # mkldnn加速仅在CPU下有效
    handle = basic.get_handle()

    # 设置要黑的卷轴名字
    target_scroll = "大地之门"         



    ops = 0
    while True:
        # break
        print(f"这是第{ops}次黑卷轴     "*4)

        # 暂离+断网+下楼
        basic.save_staute(handle)
        basic.net_state_change()
        time.sleep(4)
        basic.find_and_click(handle, "./img/common/open_door.png", 3)
        time.sleep(1)

        # 使用卷轴杀怪
        use_quake(handle)
        time.sleep(1)
        use_death_ripper(handle)
        time.sleep(1)

        # 点击宝箱
        basic.find_and_click(handle, "./img/common/scroll_box.png", 0.5)

        # 获得装备检测
        det_str_list = obtain_equip_name(handle)

        flag = False
        for ch in det_str_list:
            if ch == target_scroll:
                print("找到卷轴：", ch)
                flag = True

                basic.net_state_change()
                time.sleep(10)
                basic.save_staute(handle)


                break
        if flag:
            break
        else:
            ops+=1

            print("本次结果：", det_str_list)
            # 小SL
            basic.find_and_click(handle, "./img/common/setting.png", 1)
            basic.find_and_click(handle, "./img/common/account.png", 1)

            
            basic.find_and_click(handle, "./img/common/logout.png", 1)
            basic.net_state_change()
            time.sleep(9)
            # while True:
            #     dts = basic.match_template(handle, [basic.imread(handle, "./img/common/startgame.png")], match_threshold=0.85)
            #     if len(dts)>0:
            #         break
            
            print("开始游戏")

            basic.find_and_click(handle, "./img/common/startgame.png", 8)
            basic.find_and_click(handle, "./img/common/SLsure.png", 1)
            basic.find_and_click(handle, "./img/common/adventure.png", 7)
            time.sleep(1)
            while True:
                dts = basic.match_template(handle, [basic.imread(handle, "./img/common/setting.png")], match_threshold=0.9)
                if len(dts)>0:
                    break