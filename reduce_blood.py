import numpy as np

"""
用于神锻出图，计算需要使用的盾次数以及挨打次数

分别代表：
上星光大盾、小盾
下星光大盾、小盾
"""

small_shield_up = 559150+9354583
small_shield_down = 559150+240434
big_shield_up = 1397875+23246670
big_shield_down = 1397875+461299
hit = 117952577
all_blood = 655892

n = 40

# print(record)
# 计算将血压到10%以下所需要使用的盾次数与攻击次数

record = {}
all_record = []
for big_s_up in range(n):
    for small_s_up in range(n):
        for big_s_down in range(n):
            for small_s_down in range(n):
                blood=all_blood + big_shield_up*big_s_up + small_shield_up*small_s_up + big_shield_down*big_s_down + small_shield_down*small_s_down
                if blood<hit:
                    continue
                hit_num = blood//hit
                res_blood = blood-hit_num*hit

                use_num = small_s_down+small_s_up+big_s_down+big_s_up
                
                if 0 < blood%hit < int(all_blood*0.08):      # 不能是10%，因为铠甲会回血
                    record[res_blood] = record.get(res_blood, [])
                    record[res_blood].append([use_num, small_s_up, big_s_up, small_s_down, big_s_down, hit_num])
                    all_record.append([res_blood, use_num, small_s_up, big_s_up, small_s_down, big_s_down, hit_num])
                    # print("*"*10)
                    # print(f"使用小盾{small_s_up}次，使用大盾{big_s_up}次\n下铠甲使用小盾{small_s_down}次，使用大盾{big_s_down}次\n挨打{hit_num}次，剩余血量{res_blood}")

for k, v in record.items():
    print("*"*30)
    print(f"剩余血量为{k}的方案有：")
    print("")
    v.sort()
    for ele in v:
        # 总体操作次数大于40，过滤
        if ele[0]>60:
            continue
        print(f"总操作次数为{ele[0]}")
        print(f"使用小盾{ele[1]}次，使用大盾{ele[2]}次\n下铠甲使用小盾{ele[3]}次，使用大盾{ele[4]}次\n挨打{ele[5]}次")
        print("-"*10)

print("&"*30)
print("&"*30)
print("&"*30)
all_record.sort(key=lambda x:x[1])
print("最少次数操作：")
for i in range(min(10, len(all_record))):
    print(f"总操作次数为{all_record[i][1]}")
    print(f"使用小盾{all_record[i][2]}次，使用大盾{all_record[i][3]}次\n下铠甲使用小盾{all_record[i][4]}次，使用大盾{all_record[i][5]}次\n挨打{all_record[i][6]}次，剩余血量{all_record[i][0]}")
    print("-"*10)


print("搜索完毕")
