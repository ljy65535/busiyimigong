import basic
import cv2
import time
import numpy as np
import paddlehub as hub
import difflib



# 从左往右为行，从上到下为列         注意屏幕输入行列相反
rows = (190, 277, 364, 451, 538, 625)           # x轴 6行每行中心点坐标   190+i*87
cols = (60, 155, 250, 345, 440)                 # y轴 5列每列中心点       60+j*95
box_weight = 30                                 # Dx
box_height = 40                                 # Dy

ocr = hub.Module(name="ch_pp-ocrv3", enable_mkldnn=True)       # mkldnn加速仅在CPU下有效


class floor():
    def __init__(self, handle:basic.HANDLE, mask=None) -> None:
        self.handle = handle

        self.rows = (190, 277, 364, 451, 538, 625)           # x轴 6行每行中心点坐标   190+i*87
        self.cols = (60, 155, 250, 345, 440)                 # y轴 5列每列中心点       60+j*95
        self.box_weight = 30                                 # Dx
        self.box_height = 40                                 # Dy

        self.matrix = np.zeros((6, 5))                       # 0代表空白或者黑地板，1代表可以点击的地板
        self.mask = mask                                     # 该层掩码，表示可以忽略的地板，如神断右下
 
    # 更新当前矩阵状态
    def refresh(self, is_debug = False):
        # 截图
        img_bottom, _ = basic.get_screenshot(self.handle) 

        # 计算每一个区域的灰度均值
        light_threshold = 85       # 亮地板均值

        can_click = []              # 能够点击的候选坐标
        for i in range(6):
            for j in range(5):
                if self.mask is not None and (i, j) in self.mask:
                    continue
                start_x, end_x = self.cols[j]-self.box_height, self.cols[j]+self.box_height
                start_y, end_y = self.rows[i]-self.box_weight, self.rows[i]+self.box_weight

                part = img_bottom[start_y:end_y, start_x:end_x]

                # 模板匹配，查找远程怪或者门

                mean = cv2.mean(part)[0]
                if mean>light_threshold:
                    self.matrix[i][j] = 1           # 更新矩阵状态
                    can_click.append((i, j))

                # 调试
                if is_debug:
                    cv2.putText(img_bottom, str(round(mean)), (cols[j], rows[i]), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 3)
                    cv2.rectangle(img_bottom, (cols[j]-box_height, rows[i]-box_weight), (cols[j]+box_height, rows[i]+box_weight), (0, 0, 255))
        
        print(can_click)
        if is_debug:
            cv2.imshow("1a", img_bottom)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return can_click

        
    # 小sl
    def SL_basic(self):
        # basic.load_mumu_video(self.handle, "./img/mumu_video/小xl.mmor")
        basic.find_and_click(self.handle, "./img/common/setting.png", 1)
        basic.find_and_click(self.handle, "./img/common/account.png", 1)
        basic.find_and_click(self.handle, "./img/common/logout.png", 8)
        basic.find_and_click(self.handle, "./img/common/startgame.png", 8)
        basic.find_and_click(self.handle, "./img/common/SLsure.png", 1)
        basic.find_and_click(self.handle, "./img/common/adventure.png", 7)
        time.sleep(1)
        while True:
            dts = basic.match_template(self.handle, [basic.imread(self.handle, "./img/common/setting.png")], match_threshold=0.9)
            if len(dts)>0:
                break
    

    # 暂离+回来
    def save_staute(self):
        # 点击左上角
        print("点击左上角", end=' ')
        basic.left_mouse_click(handle=self.handle, point=(0.0902778,0.0398437), normalize=True, size=(519, 923))
        time.sleep(2)
        # 点击暂离
        print("点击暂离", end=' ')
        basic.left_mouse_click(handle=self.handle, point=(0.483333,0.958594), normalize=True, size=(519, 923))
        time.sleep(8)
        # 点击确定
        print("点击确定", end=' ')
        basic.left_mouse_click(handle=self.handle, point=(0.506944,0.7), normalize=True, size=(519, 923))
        time.sleep(1)
        # 返回迷宫
        print("返回迷宫", end=' ')
        basic.left_mouse_click(handle=self.handle, point=(0.7,0.174219), normalize=True, size=(519, 923))
        time.sleep(8)
        return 

    # 使用治疗推序1
    def use_cure_skill(self):
        time.sleep(0.5)
        print("点击右下角", end=' ', flush=True)
        basic.left_mouse_click(handle=self.handle, point=(0.854167,0.939063), normalize=True, size=(519, 923))
        time.sleep(1)
        print("点击卷轴系列", end=' ', flush=True)
        basic.left_mouse_click(handle=self.handle, point=(0.25,0.782031), normalize=True, size=(519, 923))
        time.sleep(1)
        print("点击水系魔法", end=' ', flush=True)
        basic.left_mouse_click(handle=self.handle, point=(0.913889,0.3375), normalize=True, size=(519, 923))
        time.sleep(1)
        print("点击治疗术", end=' ', flush=True)
        basic.left_mouse_click(handle=self.handle, point=(0.256944,0.357031), normalize=True, size=(519, 923))
        time.sleep(1)
        print("点击头像使用", end=' ', flush=True)
        basic.left_mouse_click(handle=self.handle, point=(0.498611,0.947656), normalize=True, size=(519, 923))
        time.sleep(1)
        # print("")
    
    # 使用神恩推序3
    def use_big_cure_skill(self):
        time.sleep(0.5)
        # print("点击右下角", end=' ')
        basic.left_mouse_click(handle=self.handle, point=(0.854167,0.939063), normalize=True, size=(519, 923))
        time.sleep(1)
        # print("点击卷轴系列", end=' ')
        basic.left_mouse_click(handle=self.handle, point=(0.25,0.782031), normalize=True, size=(519, 923))
        time.sleep(1)
        # print("点击光系魔法", end=' ')
        basic.left_mouse_click(handle=self.handle, point=(0.918056,0.592187), normalize=True, size=(519, 923))
        time.sleep(1)
        # print("点击神恩术", end=' ')
        basic.left_mouse_click(handle=self.handle, point=(0.279167,0.509375), normalize=True, size=(519, 923))
        time.sleep(1)
        # print("点击头像使用", end=' ')
        basic.left_mouse_click(handle=self.handle, point=(0.498611,0.947656), normalize=True, size=(519, 923))
        time.sleep(1)
        # print("")
    
    # 神锻黑尸体
    def SL_body(self)->bool:
        # 检查尸体位置
        dts = basic.match_template(self.handle, 
                                    [basic.imread(self.handle, './img/shenduan/body.png'), 
                                        basic.imread(self.handle, "./img/shenduan/body_9.png"),
                                        basic.imread(self.handle, "./img/shenduan/weapenpile.png")], match_threshold=0.85)
        
        if len(dts)==0:
            print("没有检测到尸体，请手动输入尸体坐标(左上角为第一行第一列[1,1]):")
            pos = tuple(map(int, input().split()))
            assert 0<pos[0]<7 and 0<pos[1]<7, "输入坐标有误"
            dts = [basic.position_trans(self.handle, pos)]

        print("尸体像素位置：", dts)
        
        print("找到尸体")
        print("*"*35)
        print("开始黑尸体")

        order = 0
        while True:     
            print(f"第{order}次   "*5)
            
            # # 使用神恩
            # for ops in range(order//3):
            #     print(f"使用{ops+1}次神恩术")
            #     self.use_big_cure_skill()
            
            # # 使用治疗
            # for ops in range(order%3):

            #     print(f"使用{ops+1}次治疗术")
            #     self.use_cure_skill()

            # 直接治疗术
            for ops in range(order):
                print(f"使用{ops+1}次治疗术")
                self.use_cure_skill()

            print("推序完成")

            # 点击尸体并翻找
            basic.left_mouse_click(handle=self.handle, point=dts[0])
            time.sleep(1)
            while True:
                find_dts = basic.match_template(self.handle, [basic.imread(self.handle, './img/shenduan/find.png')], match_threshold=0.8)
     
                if len(find_dts)>0:
                    break
            basic.left_mouse_click(handle=self.handle, point=find_dts[0])

            # 检测是否为日光
            result = self.text_identify("日光刻印")
            if result:
                break

            order+=1
            print("没找到,开始小sl")

            self.SL_basic()

        
        return True


    

    # 检测装备栏上方的文字,5s内检测
    def text_identify(self, tar_txt)->bool:
        start_time = time.time()
        area = ((0.0747222,0.851094), (0.168889,0.913281))  

        index = 0
        print("开始检测")
        while True:
            _, img = basic.get_screenshot(self.handle)
            h, w, _ = img.shape
            top, down, left, right = int(area[0][1]*h), int(area[1][1]*h), int(area[0][0]*w), int(area[1][0]*w)
            area_img = img[top:down, left:right, :]
            
            result = ocr.recognize_text(images=[area_img])
            
            now_time = time.time()
            cv2.imwrite(f'./temp/{index}.png', area_img)
            index += 1
            if len(result[0]['data']) > 0:
                # cv2.imwrite(f'./temp/{index}.png', area_img)

                det_texts = result[0]['data'][0]['text']
                print("检测到：", det_texts, flush=True)

                if tar_txt[0] == det_texts[0]:
                    print("找到！！！")
                    return True
                elif len(det_texts)==0:
                    continue
                elif  det_texts[0] in "骑日月星信猎神性失败":
                    # print(f"不符合: {tar_txt}")
                    return False
                        
                    
            if now_time-start_time>3.5:
                print("时间到！")
                return False

            

            # cv2.imshow("1a", area_img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()


    # 用于黑水池，检测天下布武
    def check_buwu(self)->bool:
        # start_time = time.time()
        area = ((0.28,0.318), (0.7166666,0.362))      # 天下布武截图区域


        # _, img = basic.get_screenshot(handle)
        # h, w, _ = img.shape
        # top, down, left, right = int(area[0][1]*h), int(area[1][1]*h), int(area[0][0]*w), int(area[1][0]*w)
        # area_img = img[top:down, left:right, :]

        # cv2.imshow("1a", area_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # return True

        print("开始截图 ")
        screenshot_list = []

        
        for i in range(10):
            _, img = basic.get_screenshot(self.handle)
            h, w, _ = img.shape
            top, down, left, right = int(area[0][1]*h), int(area[1][1]*h), int(area[0][0]*w), int(area[1][0]*w)
            area_img = img[top:down, left:right, :]
            screenshot_list.append(area_img)

            cv2.imwrite(f"./temp/temp/{i}.png", area_img)
            time.sleep(0.1)

        print("开始检测")
        result_list = ocr.recognize_text(images=screenshot_list)
        # print(result_list)
        for result in result_list:
            if len(result['data'])==0:
                continue
            det_texts = result['data'][0]['text']
            conf = difflib.SequenceMatcher(None, det_texts, "发动！天下布武").quick_ratio()  # 文本相似度匹配
            if conf>0.7:
                print("出现！天下布武")
                return True
        
        print("没有出现")
        return False
    

    def SL_pool(self)->bool:
        # 检查水池位置
        dts = basic.match_template(self.handle, 
                                   [basic.imread(self.handle, './img/shenduan/pool.png')], match_threshold=0.85)
        
        if len(dts)==0:
            print("没有检测到水池，请手动输入水池坐标(左上角为第一行第一列[1,1]):")
            pos = tuple(map(int, input().split()))
            assert 0<pos[0]<7 and 0<pos[1]<7, "输入坐标有误"
            dts = [basic.position_trans(self.handle, pos)]

        # if pos is None:
            # dts = basic.match_template(self.handle, 
            #                        [basic.imread(self.handle, './img/shenduan/pool.png')], match_threshold=0.85)
        # else:
        #     dts = [basic.position_trans(self.handle, pos)]


        print("水池像素位置：", dts)
        
        print("找到水池")
        print("*"*35)
        print("开始黑水池")

        order = 0
        while True:     
            print(f"第{order}次   "*5)
            
            # 使用神恩
            for ops in range(order//3):
                print(f"使用{ops+1}次神恩术")
                self.use_big_cure_skill()
            
            # 使用治疗
            for ops in range(order%3):

                print(f"使用{ops+1}次治疗术")
                self.use_cure_skill()

            # 直接治疗术
            # for ops in range(order):
            #     print(f"使用{ops+1}次治疗术")
            #     self.use_cure_skill()

            print("推序完成")

            # 点击尸体并翻找
            basic.left_mouse_click(handle=self.handle, point=dts[0])
            time.sleep(1)
            while True:
                find_dts = basic.match_template(self.handle, [basic.imread(self.handle, './img/shenduan/wash.png')], match_threshold=0.85)
                if len(find_dts)>0:
                    break
            basic.left_mouse_click(handle=self.handle, point=find_dts[0])
            time.sleep(0.1)

            # 检测是否为日光
            result = self.check_buwu()
            if result:
                break

            order+=1
            print("没找到,开始小sl")

            self.SL_basic()

        
        return True







# if __name__ == "__main__":  
    # handle = basic.get_handle()

    # img = basic.get_screenshot(handle)
    # print(img.shape)  # (883, 496)

    # now_floor = floor(handle)

    
    # now_floor.SL_body()
    # now_floor.SL_pool()

    # now_floor.SL_body((6,3))
    # now_floor.SL_pool((1,4))







    # now_floor.use_big_cure_skill()
    
    
    # now_floor.use_cure_skill()
    # now_floor.SL_basic()



    # now_floor.text_identify("月光刻印")

    # img_g, img_z  = basic.get_screenshot(handle)
    # print(1)
    # reader = easyocr.Reader(['ch_sim'], gpu=True)
    # result = reader.readtext(img)
    # print(result)


    # now_floor.text_identify()
    # now_floor.use_cure_skill()
    # now_floor.SL_basic()
    # print(now_floor.save_staute())
    # print(now_floor.save_staute())
    # ans = now_floor.refresh(is_debug=True)
    # print(now_floor.goto_next_floor())


