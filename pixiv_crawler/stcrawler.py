import aiofiles
import asyncio
import aiohttp
import time
import threading
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import requests
from multiprocessing import Process

headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }

url = 'https://iw233.cn/API/Random.php'

def num_gen():
    for i in range(391,100000):
        yield i

async def aiodownload(url,num):
    name = f'{num}.jpg'
    # connector = aiohttp.TCPConnector(limit = 50) # 默认可以100条连接
    timeout = aiohttp.ClientTimeout(total=600)  # 将超时时间设置为600秒
    connector = aiohttp.TCPConnector(force_close=True)  # 禁用 HTTP keep-alive
    async with aiohttp.ClientSession(headers=headers, connector=connector, timeout=timeout) as session:
        async with session.get(url) as resp:
            async with aiofiles.open(f'./st_repository/{name}','wb') as fp:
                await fp.write(await resp.content.read())
                print(name,' download finished')

gen = num_gen()

async def asyncio_tasks():
    tasks = []
    global gen
    for i in range(30):
        num = next(gen)
        tasks.append(aiodownload(url,num))
    await asyncio.wait(tasks)

class MyThread(threading.Thread):
    def __init__(self):
        super(MyThread, self).__init__()

    def run(self) -> None:
        print('开启线程')
        asyncio.run(asyncio_tasks())
        print('结束线程')

def download_one_st():
    resp = requests.get(url,headers=headers)
    name = f'{next(gen)}.jpg'
    with open(f'./st_repository/{name}','wb') as f:
        f.write(resp.content)
        f.close()
    print(name,' download complete!')

def download_one_st_30():
    for i in range(30):
        resp = requests.get(url,headers=headers)
        name = f'{next(gen)}.jpg'
        with open(f'./st_repository/{name}','wb') as f:
            f.write(resp.content)
            f.close()
        print(name,' download complete!')

class MultiOneProcess(Process):
    def __init__(self):
        super(MultiOneProcess, self).__init__()

    def run(self) -> None:
        print('进程开始')
        asyncio.run(asyncio_tasks())
        print('进程结束')


if __name__ == '__main__':
    start_time = time.time()

    # 使用线程池的做法(没有意义,还是一个cpu)
    # with ThreadPoolExecutor(3) as t:
    #     t.submit(asyncio.run(asyncio_tasks()))
        # for i in range(3):
        #     t.submit(asyncio.run(asyncio_tasks()))

    # 单线程异步 45s
    # asyncio.run(asyncio_tasks())

    # 开30个线程实现并发:
    # 83s 30张 出现了没下载完的情况
    # with ThreadPoolExecutor(30) as t:
    #     for i in range(30):
    #         t.submit(download_one_st) #加入到执行任务列表中

    #错误的,这个只用了一个线程 178s 30张
    # with ThreadPoolExecutor(30) as t:
    #     t.submit(download_one_st_30) #submit是立即返回的

    #如果python能将多个线程部署到多个cpu上那么才能实现我们想要的3个线程同步执行3个异步任务,但是GIL的存在让python不能做到这一点
    #如果使用多进程:(理论45s90张)实际: 201s 更长了
    # with ProcessPoolExecutor(3) as p:
    #     for i in range(3):
    #         p.submit(asyncio.run(asyncio_tasks()))

    #不对劲,对于异步任务他没有立即返回,而是等待30个执行完了以后才继续下面30个
    #所以究竟怎么样才能让异步任务在不同进程上直接返回呢?
    p_list = []
    for i in range(3):
        p = MultiOneProcess()
        p.start()
        p_list.append(p)

    for p in p_list:
        p.join()







    # 创建线程进行操作 145s
    # t1 = MyThread()
    # t2 = MyThread()
    # t3 = MyThread()
    #
    # t1.start()
    # t2.start()
    # t3.start()
    # t1.join()
    # t2.join()
    # t3.join()

    print(time.time()-start_time)

