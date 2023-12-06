import base64
import json
import os.path

import requests
import time

GET_DIR_URL = 'A'
BASE_DOWN_URL = 'B'
STORE_FILE_BASE = '/Users/michael/Downloads/python/'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Host': 'pingkai.myqnapcloud.com:5245',
    # 'Origin': 'https://pingkai.myqnapcloud.com:5245',
    # 'Referer': 'https://pingkai.myqnapcloud.com:5245'
}


def download_all_books(path):
    session = requests.Session()
    get_dir_books(session, path)


def get_dir_books(session, path):
    post_data = {
        'path': '/aliyunCloud/' + path,
        'password': '',
        'page': 1,
        'per_page': 0,
        'refresh': False
    }
    try:
        response = session.post(GET_DIR_URL, data=post_data, headers=HEADER)
    except Exception as e:
        print('get dir books exp : ' + str(e) + '\n' + path)
    if response and response.status_code == 200:
        books = json.loads(response.text)['data']['content']
        if books:
            for book in books:
                if book['is_dir']:
                    # if book['name'] == 'dir_already_download':
                    #     continue
                    get_dir_books(session, path + '/' + book['name'])
                else:
                    download_book(session, path, book['name'])
        else:
            print('cant get dir books : ' + path)
    else:
        print('get dir books error : ' + str(e) + '\n' + path)


def download_book(session, file_path, file_name):
    if not os.path.exists(STORE_FILE_BASE + file_path):
        os.makedirs(STORE_FILE_BASE + file_path, exist_ok=True)
    try:
        response = session.get(BASE_DOWN_URL + file_path + '/' + file_name)
    except Exception as e:
        print('download book exp : ' + str(e) + '\n' + file_path)
    if response and response.status_code == 200:
        try:
            with open(STORE_FILE_BASE + file_path + '/' + file_name, 'wb') as f:
                f.write(response.content)
            time.sleep(3)
        except Exception as e:
            print('write book exp : ' + str(e) + '\n' + file_path)
    else:
        print('download book error : ' + str(e) + '\n' + file_path)


def encode_decode_url(url):
    enc_url = base64.b64encode(url.encode(encoding='utf-8'))
    print(enc_url)
    # URL_A   b'aHR0cHM6Ly9waW5na2FpLm15cW5hcGNsb3VkLmNvbTo1MjQ1L2FwaS9mcy9saXN0'
    # URL_B  b'aHR0cHM6Ly9waW5na2FpLm15cW5hcGNsb3VkLmNvbTo1MjQ1L2QvYWxpeXVuQ2xvdWQv'
    dec_url = base64.b64decode(enc_url).decode(encoding='utf-8')
    print(dec_url)


if __name__ == '__main__':
    url = ''
    url_2 = ''
    encode_decode_url(url)
    encode_decode_url(url_2)

    # path = 'python教程合集/【Python电子图书集合】'
    # download_all_books(path)
