import requests
domain = 'http://api.lngqt.shechem.cn/webapi/learn/addlearnlog'

headers = {
    'Cookie':'BDed_HeaderKey=DWxbB3ELFCgoK3IeH1JxUSl3fhIIBVVHUHh9KTEWW14PQENcVhQ%3D',
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/3.3.1(0x13030110) Safari/605.1.15 NetType/WIFI',
    'Referer' : 'http://websecond.lngqt.shechem.cn/'
}

resp = requests.post(domain,headers=headers)
print(resp.text)