import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import csv

f = open('bangumi.csv', mode = 'w',encoding = 'utf-8')
csvwriter = csv.writer(f)

def one_page(page):
    url = f'http://bangumi.tv/anime/browser?sort=rank&page={page}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }
    resp = requests.get(url,headers=headers)
    resp.encoding = 'utf-8'

    html = etree.HTML(resp.text)

    lis = html.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/ul/li')
    for li in lis:
        name = li.xpath('./div/h3/a/text()')[0]
        info  = li.xpath('./div/p[1]/text()')[0].replace(' ','')
        info = info.replace('\n','')
        rank = li.xpath('./div/p[2]/small/text()')[0]
        comment = li.xpath('./div/p[2]/span/text()')[0]
        csvwriter.writerow([name,info,rank,comment,page])
    print(f'page{page} finished!')

if __name__ == '__main__':
    with ThreadPoolExecutor(30) as t :
        for i in range(1,100):
            t.submit(one_page,i)