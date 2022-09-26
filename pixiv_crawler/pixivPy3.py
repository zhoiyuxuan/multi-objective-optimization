import pixivpy3.utils
import time
import random
from pixivpy3 import *
from pixiv_auth import *

api = AppPixivAPI()
_REFRESH_TOKEN_OLD = 'egf7Xdj9VHqMVqL42ByWSxRxzr51Nxf2rLvmN7-Nja4'
_REFRESH_TOKEN = 'egf7Xdj9VHqMVqL42ByWSxRxzr51Nxf2rLvmN7-Nja4'
# _REFRESH_TOKEN = refresh(_REFRESH_TOKEN_OLD)
time.sleep(5)

#登录(如果报错注释掉再运行)
while True:
    try:
        api.auth(refresh_token=_REFRESH_TOKEN)
        break
    except pixivpy3.utils.PixivError:
        print('refresh token error, restarting...')
        r = random.randint(20,60)
        time.sleep(r)

# 批量下载某位画家画作 (更改directory和auth_id即可)
auth = 'KinHasu'
auth_id = 29067454
total_num = 240
directory = f'./{auth}'
enum = int(total_num/30)


for i in range(0,enum):
    json_result = api.user_illusts(auth_id,offset=30*i)
    print('get json_result success!')
    for illust in json_result.illusts:
        print("[%s] %s" % (illust.title, illust.image_urls.large))
        api.download(illust.image_urls.large,path=directory)

