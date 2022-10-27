import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor


url = f'https://www.huiwenwang.cn/fileroot1/2020-11/19/93773d77-b958-4f27-9407-0e98414a1491/93773d77-b958-4f27-9407-0e98414a149'
headers = {
        'Referer':'https://www.huiwenwang.cn/p-1609489.html',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}



def download_one_page(url,i):
    resp = requests.get(url, headers=headers)
    with open(f'./linear/{i-10}.gif','wb') as f:
        f.write(resp.content)
    print(f'{i-10} finished!')
    f.close()

with ThreadPoolExecutor(50) as t:
    for i in range(11, 91):
        download_one_page(url+f'{i}.gif',i)
    print(f'page {i-10} download complete!')