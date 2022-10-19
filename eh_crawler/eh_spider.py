import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor


url = 'https://e-hentai.org/g/2336353/8512716342/'
headers = {
        'Referer':'http://g.e-hentai.org/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}
child_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}



def download_one_page(url):
    resp = requests.get(url, headers=headers)
    tree = etree.HTML(resp.text)
    urls = tree.xpath('//*[@id="gdt"]/div')
    for url in urls:
        child = url.xpath('./div/a/@href')[0]
        resp_child = requests.get(child,headers=child_headers)
        tree_child = etree.HTML(resp_child.text)
        img_url = tree_child.xpath('//*[@id="img"]/@src')[0]

        title = img_url.split('/')[-1]
        resp_img = requests.get(img_url,headers=child_headers)
        with open(f'{title}.jpg','wb') as f:
            f.write(resp_img.content)
        print(f'{title} finished!')
        f.close()


with ThreadPoolExecutor(50) as t:
    for i in range(1, 3):
        download_one_page(url+f'?p={i}')
    print(f'page {i} download complete!')