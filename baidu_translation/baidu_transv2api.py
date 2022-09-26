# 2022-09-25 有效
import execjs
import requests
def get_v2api_result(query,source='en',dest='zh'):
    url_sentence_e2c = f'https://fanyi.baidu.com/v2transapi?from={source}&to={dest}'
    # headers 必须带 Cookie，百度翻译的反扒手段之一
    headers = {
        'Cookie': 'BIDUPSID=E1D5C51AAE1E2FB61B92B317F52B0A24; PSTM=1581325017; __yjs_duid=1_fc740a5290a9113cf233bb2a8432d5151619450553193; MCITY=-%3A; BAIDUID=8938DB37269370AAB7F367842BAE255B:SL=0:NR=10:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=tUTENGNVpaNGk1enNvTVo5NFd4RzBSTUdoUFBpQmJqaXh0Wkdiak1PSTJPRkpqSVFBQUFBJCQAAAAAAAAAAAEAAAAJnwmIbGFsYWZm1q646AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADarKmM2qypjZk; BDUSS_BFESS=tUTENGNVpaNGk1enNvTVo5NFd4RzBSTUdoUFBpQmJqaXh0Wkdiak1PSTJPRkpqSVFBQUFBJCQAAAAAAAAAAAEAAAAJnwmIbGFsYWZm1q646AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADarKmM2qypjZk; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1664113149; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1664113149; ab_sr=1.0.1_NzJkM2M0MjliZjAxOTQ2ZWVmODI4ODA2Zjk5NzY4MmQ5ZGRkMTgzOWZmZjhiYjBkOTU5M2E1ZTNhMTcxNzM4MzAzNDI3NzA1NjNiZGIxZGIxYmVjNGY3M2VkY2I2OTVkYmVjZWFmNWUwZDA1MzE4NWZmYWEwMWNiZDI0MzAzZmYyYWQ5ODZkYjRmYzE0ODFjZDA5Y2QzYjU1M2MxN2VmNjRkMTAyZTNjMGEzMGU3ZDU2YmI3Njg2MmZmYjY0NzQ4; delPer=0; PSINO=1; BAIDUID_BFESS=8938DB37269370AAB7F367842BAE255B:SL=0:NR=10:FG=1; BA_HECTOR=2g812ka48ga481a4a1ah0g5e1hj0nvn18; ZFY=sWm0LzgwlPvDm00nJ:AkPNiXROQlbmxIW9bTxyQEvDH0:C; H_PS_PSSID=37156_36547_36466_37114_37353_37491_37299_36884_34812_37486_37407_36789_37260_26350_37479_22157'
    }
    # 生成 sign
    with open('/Users/tommyzhou/Desktop/tool/baidu_translation/pGrab.js', mode='r', encoding='utf-8') as f:
        sign = execjs.compile(f.read()).call("tl", query)
    # 表单数据，将第二步中的kv全部复制过来
    data = {
        'from': source,
        'to': dest,
        'query': query,
        'simple_means_flag': '3',
        'sign': sign,
        'token': '4910354847389a6d0ed7ca8ed85b77f6',
        'domain': 'common'
    }
    resp = requests.post(url_sentence_e2c, data = data, headers=headers)
    #打印翻译结果
    print(resp.json()['trans_result']['data'][0]['dst'])