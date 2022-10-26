chang = [7,15,10,11,9,14,13]
kuan = [6,1,7]

square=0
area = []

for i in chang:
    for j in kuan:
        area.append(i*j)
        if i ==j:
            print(f'皮皮拼出了一个{i}x{j}的特殊正方形,面积为{i*j}')
            square+=1
        else:
            print(f'皮皮拼出了一个{i}x{j}的一般长方形,面积为{i * j}')

print(f'有{square}个特殊正方形')
print(f'其中面积最大是{max(area)},面积最小是{min(area)}')