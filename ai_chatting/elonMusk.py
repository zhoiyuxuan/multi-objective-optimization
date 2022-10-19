# based on beta.character.ai
import requests
import re

url = 'https://server.character.ai/chat/streaming/'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'referer' : 'https://beta.character.ai/',
    'authorization' : 'Token a8b552497634ddc6dee58b67da4dac6ce601544e'
}

print('Hello! This is Elon Musk. What would you like to ask?')
while True:
    ask = input('>>')
    if ask == 'quit' or'exit':
        break

    data = {
        'character_external_id':"zv4QeeU8u7xjkrtwPRshFEsrJus87AkSTes3A5pfsoE",
        'history_external_id' : '5qX3lNjXXg1EnzqzEjS9_F9PCQwotxuNqc4ceuddgQU',
        'text':ask,
        'tgt':'internal_elon',
        'ranking_method':'random',
        'is_proactive': False
    }
    resp = requests.post(url,data = data ,headers = headers)

    obj = re.compile(r'"text": "(?P<reply>.*?)"')
    result = obj.finditer(resp.text)
    replys = []
    for it in result:
        reply = it.group('reply')
        if reply.endswith('.') and reply not in replys:
            reply.replace('"','')
            replys.append(reply.replace(r'\n',''))

    print(replys[0],'\n')
