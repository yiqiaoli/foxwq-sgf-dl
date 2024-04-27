import requests
from urllib.parse import urlencode


def get_image_recognition_reserve(uid, path):
    url = "https://judge.foxwq.com/judge/AutoRecognitionGo_Multipart"
    files = [
        ('cmd', (None, 'submit')),
        ('qipan', (None, '19')),
        ('uid', (None, uid)),
        ('webskey', (None, '')),
        ('gameid', (None, '369')),
        ('accounttype', (None, '2')),
        ('clienttype', (None, '64')),
        ('picture', ('test.jpg', open(path, 'rb'), 'image/jpeg'))
    ]
    response = requests.post(url, files=files)
    return response.json()['Reserve']


def image_recognition_result(uid, reserve):
    url = 'https://judge.foxwq.com/judge/AutoRecognitionGoResult_Multipart'
    headers = {
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded',
        'accept-encoding': 'gzip, deflate, br',
        'x-unity-version': '2022.1.16f1',
        'user-agent': 'yhwqHD/4 CFNetwork/1494.0.7 Darwin/23.4.0',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '103',
        'cookie': '_ga=GA1.1.1809022198.1701614345; _ga_RJZVB1BZBR=GS1.1.1702205836.2.1.1702205985.0.0.0'}

    form_data = {'cmd': 'get',
                 'uid': uid,
                 'uin': '0',
                 'webskey': '',
                 'gameid': '369',
                 'accounttype': '2',
                 'clienttype': '64',
                 'reserve': reserve
                 }
    encoded_data = urlencode(form_data, safe='').encode('utf-8')
    response = requests.post(url, data=encoded_data, headers=headers)
    return response.json()


if __name__ == '__main__':
    uid = '531095793'
    path = 'test.jpg'
    reserve = get_image_recognition_reserve(uid, path)
    print(reserve)
    print(image_recognition_result(uid, reserve))
