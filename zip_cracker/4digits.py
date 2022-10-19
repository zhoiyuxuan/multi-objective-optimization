import zipfile
import time
import threading

startTime = time.time()
# 判断线程是否需要终止
flag = True


def extract(password, file):
    try:
        password = str(password)
        file.extractall(path='.', pwd=password.encode('utf-8'))
        print("the password is {}".format(password))
        nowTime = time.time()
        print("spend time is {}".format(nowTime - startTime))
        global flag
        # 成功解压其余线程终止
        flag = False
    except Exception as e:
        print(e)

alpha = 'a b c d e f g h i'

def do_main():
    zfile = zipfile.ZipFile("/Users/tommyzhou/Downloads/photoshop2021_22.4.3/Photoshop2021.zip", 'r')
    # 开始尝试
    alpha = ['a']
    for number in range(1, 9999):
        if flag is True:
            t = threading.Thread(target=extract, args=(number, zfile))
            t.start()
            t.join()


if __name__ == '__main__':
    do_main()
