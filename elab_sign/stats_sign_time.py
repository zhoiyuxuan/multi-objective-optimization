f = open('login.txt','r')
stat={}
for i in f.readlines():
    i = i.split(' ')
    try:
        stat[i[0]] += float(i[-1].replace('\n', ''))
    except KeyError:
        stat[i[0]] = float(i[-1].replace('\n', ''))

for item,values in stat.items():
    print(f'{item} : {values}')
    if values < 5*3600:
        print('签到时长不达标')