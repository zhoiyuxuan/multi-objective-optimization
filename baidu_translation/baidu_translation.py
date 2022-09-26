import requests
import urllib.request
import urllib.parse
import execjs
import json
from baidu_transv2api import get_v2api_result
#翻译单词



headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'Cookie': 'BIDUPSID=E1D5C51AAE1E2FB61B92B317F52B0A24; PSTM=1581325017; __yjs_duid=1_fc740a5290a9113cf233bb2a8432d5151619450553193; MCITY=-%3A; BAIDUID=8938DB37269370AAB7F367842BAE255B:SL=0:NR=10:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=tUTENGNVpaNGk1enNvTVo5NFd4RzBSTUdoUFBpQmJqaXh0Wkdiak1PSTJPRkpqSVFBQUFBJCQAAAAAAAAAAAEAAAAJnwmIbGFsYWZm1q646AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADarKmM2qypjZk; BDUSS_BFESS=tUTENGNVpaNGk1enNvTVo5NFd4RzBSTUdoUFBpQmJqaXh0Wkdiak1PSTJPRkpqSVFBQUFBJCQAAAAAAAAAAAEAAAAJnwmIbGFsYWZm1q646AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADarKmM2qypjZk; delPer=0; PSINO=1; H_PS_PSSID=37156_36547_36466_37114_37353_37491_37299_36884_34812_37486_37407_36789_37260_26350_37479_22157; BAIDUID_BFESS=8938DB37269370AAB7F367842BAE255B:SL=0:NR=10:FG=1; BA_HECTOR=8laka18h0h0105810halljab1hj0mfq19; ZFY=sWm0LzgwlPvDm00nJ:AkPNiXROQlbmxIW9bTxyQEvDH0:C; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1664113149; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1664113149; ab_sr=1.0.1_NzJkM2M0MjliZjAxOTQ2ZWVmODI4ODA2Zjk5NzY4MmQ5ZGRkMTgzOWZmZjhiYjBkOTU5M2E1ZTNhMTcxNzM4MzAzNDI3NzA1NjNiZGIxZGIxYmVjNGY3M2VkY2I2OTVkYmVjZWFmNWUwZDA1MzE4NWZmYWEwMWNiZDI0MzAzZmYyYWQ5ODZkYjRmYzE0ODFjZDA5Y2QzYjU1M2MxN2VmNjRkMTAyZTNjMGEzMGU3ZDU2YmI3Njg2MmZmYjY0NzQ4',
}

def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

while True:
    s=input('>>')
    if '*' in s:
        url_word = 'https://fanyi.baidu.com/sug'
        data ={
            'kw':s.split('*')[0]
        }
        # 发送post请求,发送数据必须放在字典中,通过data参数进行传递
        resp = requests.post(url_word, data=data, headers=headers)
        print(resp.json()['data'][0]['v']) #将服务器返回的内容直接处理成json 变成dict

    elif is_contains_chinese(s):
        get_v2api_result(s,source='zh',dest='en')

    else:
        get_v2api_result(s)



