# 目标:自动爬取京东GPU价格
# 1 获得网页源代码
# 2 xpath解析获得价格\数据
# 3 线程池请求多个价格

import requests
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor
import datetime

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'cookie':'__jdu=16256595819281030731648; shshshfpa=0a622ae2-7b2b-1a47-8b0d-e894a26e6c6b-1581607728; shshshfpb=paWAu8aMEmxsA6gXcF4fZeA%3D%3D; qrsc=3; TrackID=1L66QQkSeNfVjg1mvnicqGdhynHRDRLyEEcOpU4VqLPRNATc8XOeyNMWkwMWMbjUgWCUS622cb_yEKjMVrzVFXu8O93236hiRMKMb9odc5VfLcvUmbu4NVWEHktz6szL7; pinId=kOYYWBxqjSU2S5aoHO-GTQ; unpl=JF8EAKtnNSttWExWBhgGGBEUTQ1RWw4PSx8Da2MNUg8IQgQDHlAaRxJ7XlVdXhRKHh9sbhRUWlNPUw4bAisSEXtfVVdcDkgWA25XNVNdUQYVV1YyGBIgS1xkXloLTxAHZ2MMVFVbQlQEGQMdEBBMWF1ubQ9LHjNfVwBUXFlPVwMdARMiEXtfVV9YAEkfAGZmNR8zWQZUAhgGHBYYT1RUVl4BSxYBbmEHVFpdQmQEKwE; __jdv=76161171|direct|-|none|-|1663572147965; PCSYCityID=CN_310000_310100_0; jsavif=1; jsavif=1; __jda=122270672.16256595819281030731648.1625659582.1663572148.1664013022.35; __jdb=122270672.2.16256595819281030731648|35.1664013022; __jdc=122270672; shshshfp=7da1aa7372cab9b38e507e86c1f4b2a6; shshshsID=bcf430274211124ca0d61f60fb210f1c_2_1664013031157; areaId=27; ipLoc-djd=27-2402-0-0; rkv=1.0; 3AB9D23F7A4B3C9B=SGOZFFK2VSGQHGJK26SO5ZC4O3S3BI7C7VKIZ6KARL5XPECQICTXIRGGNROCG5GH6JGO3WHMLIH5V7AP6465NHSMPY',
}
item_tags = ['3060','3090','3090ti']



def download_one_page(url):
    resp = requests.get( url ,headers = headers)
    tree = etree.HTML(resp.text)
    items = tree.xpath('//*[@id="J_goodsList"]/ul/li')
    today = datetime.date.today()

    try:
        for item in items:
            item_price = item.xpath('./div/div[2]/strong/i/text()')[0] #注意子路径的寻找用item
            item_names = item.xpath('./div/div[3]/a/em/text()')
            item_name = ''
            count = 0
            for i in item_names:
                i = i.strip()
                if count == 0:
                    item_name = f'{i} {item_tag} '
                else:
                    item_name += i
                count +=1
            # item_comment_urls = item.xpath('./div/div[4]/strong/a/@href')#这个再想想办法吧,它是通过js加载的,同时请求数据加密过,理论上用selenium比较好但是肯定永不了
            item_shop = item.xpath('./div/div[5]/span/a/text()')[0]
            csvwriter.writerow([item_price,today,item_name,item_shop])
        page = url.split('=')[-1]
        print(page, 'finished!')
    except IndexError:
        pass


if __name__ == '__main__':
    verify = input('please check if you have run today?(yes to go on)\n')
    if verify =='yes':
        for item_tag in item_tags:
            f = open(f'{item_tag}.csv', mode='a+', encoding='utf-8')
            csvwriter = csv.writer(f)
            with ThreadPoolExecutor(50) as t:
                for i in range(1,10):
                    download_one_page(f'https://search.jd.com/Search?keyword={item_tag}&page={i}')
                print(f'{item_tag} download complete!')
    else:
        print('see you again!')