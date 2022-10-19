#我发现b站上有个天天更新p站每日推荐的up主,我们去直接爬他的图片下来就ok了
import requests
import datetime
from lxml import etree
import os
from concurrent.futures import ThreadPoolExecutor

#每天改cv就可以了
cvs = ['cv18984413','cv18937414','cv18923158','cv18908075','cv18896016','cv18883224','cv18866581','cv18849168','cv18831714','cv18814038']

def download_one_cv(cv):
    url = f'https://www.bilibili.com/read/{cv}'
    headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',

            }
    resp = requests.get(url,headers=headers)

    html = etree.HTML(resp.text)
    figures = html.xpath('/html/body/div[3]/div/div[3]/div[1]/div[5]/div/figure')

    date = datetime.date.today()
    os.system(f'mkdir {date}')

    for figure in figures[1:]:
        img_url = figure.xpath('./img/@data-src')[0].replace('//','')
        img_url = f'http://{img_url}'
        img_resp = requests.get(img_url)
        img_name = img_url.split('/')[-1]
        with open(f'./{date}/'+img_name,'wb') as f:
            f.write(img_resp.content)

        print('over:',img_name)

if __name__ == '__main__':
    with ThreadPoolExecutor(50) as t:
        for cv in cvs:
            t.submit(download_one_cv, cv)

