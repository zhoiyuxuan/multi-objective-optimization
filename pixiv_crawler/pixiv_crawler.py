
'''
todo: 按照画师爬取
1 获取画师uid(手动)
2 获取页面源代码
3 处理图片url
4 get图片
5 下载图片
'''
import requests


class Artist:
    def __init__(self,name='せんちゃ',uid='3388329'):
        self.artist_name = 'せんちゃ'
        self.artist_uid = '3388329'

class Crawler:
    def __init__(self,url,referer=''):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'Referer' : referer,
        }

    def get_page_html(self):
        resp = requests.get(self.url, headers=self.headers)
        return resp

    def post_page_response(self):
        resp = requests.post(self.url, headers=self.headers)
        return resp


a = Artist()
url = f'https://www.pixiv.net/users/{a.artist_uid}/artworks'
c = Crawler()