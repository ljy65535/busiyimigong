import basic
import cv2
import time
import numpy as np
import paddlehub as hub
import difflib


# 神锻永动机融序列


# 判断是否熔炼出淬火
def check_cuihuo(handle:basic.HANDLE)->bool:
    area = ((0.13,0.318), (0.8366666,0.362))      # 截图区域

    print("开始截图并检测")
    screenshot_list = []
    for _ in range(40):
        _, img = basic.get_screenshot(handle)
        h, w, _ = img.shape
        top, down, left, right = int(area[0][1]*h), int(area[1][1]*h), int(area[0][0]*w), int(area[1][0]*w)
        area_img = img[top:down, left:right, :]
        screenshot_list.append(area_img)
        time.sleep(0.05)

    result_list = ocr.recognize_text(images=screenshot_list)
    # print(result_list)
    for result in result_list:
        if len(result['data'])==0:
            continue
        det_texts = result['data'][0]['text']

        conf = difflib.SequenceMatcher(None, det_texts, "熔炼出了奇怪的东西").quick_ratio()  # 文本相似度匹配
        if conf>0.4:
            print("淬火！")
            return True
    
    print("没有出现")
    return False


# 查找指定刻印
def find_stamp(handle, stamp_path:list):
    print("向左侧翻页，翻到第一页")



# 尝试熔炼刻印
def smelt_champ(handle:basic.HANDLE, stamp_path_list:list, if_check=True)->bool:
    # 进入炉子界面
    basic.find_and_click(handle, "./img/shenduan/stove_type2.png", 0.5)
    basic.find_and_click(handle, "./img/shenduan/add_stamp.png", 0.5)


    # 查找刻印
    while True:
        dts = basic.match_template(handle, [basic.imread(handle, path) for path in stamp_path_list], match_threshold=0.9)
        if len(dts)>0:
            basic.left_mouse_click(handle=handle, point=dts[0])
            time.sleep(1)
            break


    # 确认选择
    basic.find_and_click(handle, "./img/shenduan/choose_equip.png", 0.5)



    # 点击熔炼按钮
    basic.find_and_click(handle, "./img/shenduan/stove_bottom_stamp.png", 0.5)

    if if_check == False:
        basic.find_and_click(handle, "./img/shenduan/back.png", 0.5)        # 点击返回按钮
        # 跳过检测
        return False
    
    # 检测结果  出则暂离保存
    result = check_cuihuo(handle)

    basic.find_and_click(handle, "./img/shenduan/back.png", 0.5)        # 点击返回按钮
    if result:
        basic.find_and_click(handle, "./img/shenduan/pool.png", 0.5)
        basic.find_and_click(handle, "./img/shenduan/pool_wash.png", 0.5)

        
    else:
        print("小sl,使用普通刻印推进序列")
        # 没出则sl+垫暂离
        basic.SL_basic(handle)

        # 融垃圾刻印推序
        smelt_champ(handle, ["./img/stamp/stamp1.png", "./img/stamp/stamp2.png", "./img/stamp/stamp3.png"], if_check=False)
    

    # 暂离保存
    basic.save_staute(handle)
    return result
    




if __name__ == "__main__":  
    ocr = hub.Module(name="ch_pp-ocrv3", enable_mkldnn=True)       # mkldnn加速仅在CPU下有效
    handle = basic.get_handle()

    # for i in range(10):
    #     print("-"*30)
    #     print(i)
    #     smelt_champ(handle)

    # basic.find_and_click(handle, "./img/stamp/stamp1.png", 0.5, 0.9)

    ops = 0
    for i in range(100):
        print(f"这是第{i}次熔炼    "*4)
        smelt_result =  smelt_champ(handle, ["./img/stamp/stamp0.png"], True)
        if smelt_result:
            ops+=1
        print(f"当前{i}次， 淬火熔炼{ops}次")

    