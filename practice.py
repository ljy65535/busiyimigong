import numpy as np
import json
import basic
import time

# a = np.array([[1,2], [3, 4]])
# b = a.pop()
# print(b)


# import torch
# print(torch.__version__)
# print(torch.cuda.is_available())

import cv2
# a = np.ones((100, 100))
# index = "啊"
# # index = "a"
# cv2.imwrite(f'./temp/{index}.png', a)
# x = torch.rand(5, 3)

# print(x)

# handle = basic.get_handle()
# basic.load_mumu_video(handle, "./img/mumu_video/小xl.mmor")
# basic.load_mumu_video(handle, "./77.mmor")
# resolution_x, resolution_y = handle.right-handle.left, handle.bottom-handle.top

# with open("./77.mmor", "r", encoding='gb18030', errors='ignore') as f:
#     data = f.read()
#     actions = eval(data)['actions']

#     for ele in actions[1:-1]:
#         # print(ele)
#         ele_data = ele['data']
#         timing = int(ele['timing'])//1000+1
#         print(f"休息{timing}秒")
#         time.sleep(timing)
#         if ele_data!='release':
#             point_str = ele_data.split(":")[1][1:-1]
#             dx, dy = list(map(float, point_str.split(",")))
#             x, y = int(dx*resolution_x), int(dy*resolution_y)
#             basic.left_mouse_click(handle, (x, y))
#             print(f"点击({x},{y})")
            # print((x, y), timing)


        
        # print(ele_data, timing)


# data = json.load("./77.mmor")
# print(data)

# cv2.imshow("1a", area_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# import easyocr
# import paddlehub as hub
# # reader = easyocr.Reader(['ch_sim'])

# # img = cv2.imread("./temp/a.png")
# # img = cv2.imread("./temp/66.png")
# img = cv2.imread("./temp/aa.png")


# ocr = hub.Module(name="ch_pp-ocrv3", enable_mkldnn=True)       # mkldnn加速仅在CPU下有效
# result = ocr.recognize_text(images=[img])
# print(result[0]['data'])


# img = cv2.resize(img, (img.shape[1]*5, img.shape[0]*5))
# lower_blue = np.array([110, 50, 50])
# upper_blue = np.array([130, 255, 255])
# mask = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), lower_blue, upper_blue)
# blue_img = cv2.bitwise_and(img, img, mask)

# img = cv2.imread("./temp/11.png")
# img = cv2.imread("./temp/66.png", cv2.IMREAD_GRAYSCALE)
# print(img.shape)
# img = img[:, :30, :]
# background = cv2.imread("./temp/1.png")

# new_img = img-background
# new_img=cv2.blur(new_img,(2,2))

# ret, binary = cv2.threshold(new_img, 140, 255, cv2.THRESH_BINARY)

# cv2.imshow("1a", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# result = reader.readtext(img)
# result = reader.readtext(img, allowlist="骑士猎人信徒月星日光刻印", text_threshold=0.2, low_text=0.2, mag_ratio=10, adjust_contrast =0.5  )
# result = reader.readtext(img, allowlist="骑士猎人信徒日月星光刻印", text_threshold=0.2, low_text=0.1, add_margin=0.1 )
# print(result)
# # print(result[0])

# img = cv2.rectangle(img, (result[0][0][0][0], result[0][0][0][1]), (result[0][0][2][0], result[0][0][2][1]), (0,255,0), 2)
# cv2.imshow("1a", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


################### 截图###################
# handle = basic.get_handle()
# print(f"底部{handle.bottom}, 顶部{handle.top}, 左边{handle.left}, 右边{handle.right}, 高{handle.bottom-handle.top}, 长{handle.right-handle.left}")
# b, a = basic.get_screenshot(handle)

# print(a.shape)
# print(b.shape)

# new_a = cv2.resize(a, (handle.right-handle.left, handle.bottom-handle.top))
# print(new_a.shape)
# cv2.imshow("1a", new_a)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



# result = [(i, j) for i in range(6) for j in range(6)]
# print(result)

# a = ['./temp/']
# for ele in a:
#     print(ele)

# a = []

# a.append([1,2])
# print(a)


# # 文字识别
# import paddlehub as hub
# import difflib
# ocr = hub.Module(name="ch_pp-ocrv3", enable_mkldnn=True) 
# a = cv2.imread("./temp/82.png")
# print(a.shape)
# a = cv2.resize(a, (a.shape[0]*2, a.shape[1]*2))
# print(a.shape)

# img1 = cv2.imread("./img/temp/a.png")
# img2 = cv2.imread("./img/temp/b.png")
# img3 = cv2.imread("./img/temp/c.png")
# img4 = cv2.imread("./img/temp/d.png")
# img5 = cv2.imread("./img/temp/e.png")
# time0 = time.time()
# # result = ocr.recognize_text(images=[img1, img2, img3, img4, img5])
# result = ocr.recognize_text(images=[a])

# print(result)

# for r in result:
#     if len(r['data'])==0:
#         print(r, "空的")
#         continue
#     det_texts = r['data'][0]['text']
#     conf = difflib.SequenceMatcher(None, det_texts, "发动！天下布武").quick_ratio() 
#     print(det_texts, conf)

# det_texts = result[0]['data'][0]['text']
# time1 = time.time()
# a = difflib.SequenceMatcher(None, det_texts, "发动！天下布武").quick_ratio()
# time2 = time.time()
# print(det_texts)
# print(a)
# print(time1-time0, time2-time1)


# seq_101 = np.zeros((101), dtype=int)
# print(seq_101, seq_101.shape)

# import os
# equipments_path = {"1":["./img/equipments/1level/" + path for path in os.listdir("./img/equipments/1level/")], 
#                    "2":["./img/equipments/2level/" + path for path in os.listdir("./img/equipments/2level/")],
#                    "3":["./img/equipments/3level/" + path for path in os.listdir("./img/equipments/3level/")],
#                    "4":["./img/equipments/4level/" + path for path in os.listdir("./img/equipments/4level/")],
#                    "5":["./img/equipments/5level/" + path for path in os.listdir("./img/equipments/5level/")],
#                    "6":["./img/equipments/6level/" + path for path in os.listdir("./img/equipments/6level/")]}

# def save_seq(seq101, flag_txt=""):
#     with open("./seq101.txt", "a") as f:
#         if len(flag_txt)>0:
#             f.writelines(flag_txt + "\n")
#         f.writelines(time.asctime()+ "\n")

#         temp_record = ""
#         for ch in seq101:
#             if str(ch) == "0":
#                 temp_record+="x"
#             else:
#                 temp_record+=str(ch)
#                 f.writelines(str(len(temp_record)-1) + "   "+ temp_record + "\n")
#                 temp_record = ""
#         if len(temp_record)>0:
#             f.writelines(str(len(temp_record)) + "   "+ temp_record + "\n")

#         for _ in range(3):
#             f.writelines("\n")

# save_seq([0,0,0,0,1,0,0,1,2,3,0,0,0,0,0,0,1,0,0,0], "这是一条测试序列")

# print(f"{123}abc")
# 假设你有三个序列
# seq1 = [1, 0, 3, 0, 5, 0, 7, 0, 9, 0, 11, 0, 13, 0, 15, 0, 17, 0, 19, 0]
# seq2 = [0, 2, 0, 4, 0, 6, 0, 8, 0, 10, 0, 12, 0, 14, 0, 16, 0, 18, 0, 20]
# seq3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# # 将三个序列合并并取不为0的最小值
# # result_sequence = [min(x, y, z) for x, y, z in zip(seq1, seq2, seq3)]

# result_sequence = [(x,y,z) for x, y, z in zip(seq1, seq2, seq3)]
# print(result_sequence)

# # a = np.ones((5), dtype=int)
# a = [1,2,3,4,5]
# with open("./temp.txt", "w") as f:
#     f.writelines(str(a))

# for i in range(0):
#     print("&&&")

print((5/6)**30)

