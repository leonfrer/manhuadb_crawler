from urllib import request
from bs4 import BeautifulSoup
import os
import re
import base64
import json
import time
import threading
import sys
import requests

request_head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'}
base_url = "https://www.manhuadb.com"
opener = request.build_opener()
opener.addheaders = [
    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0')]
request.install_opener(opener)

headers = {
    'Host': 'i1.manhuadb.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Accept': 'image/avif,image/webp,*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.manhuadb.com/',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers'
}


def download_book_from_link(link: str, parent_path: str):
    print(link, parent_path)
    sub_url = base_url + link
    img_base_url = ('https://i1.manhuadb.com/ccbaike' +
                    link).replace('_', '/').replace('.html', '/')
    img_base_url = re.sub(r'/manhua/[^/]*', '', img_base_url)
    sub_soup = BeautifulSoup(request.urlopen(request.Request(url=sub_url, headers=request_head)).read(), 'html.parser')
    sub_title = sub_soup.select_one('body > div.container-fluid.comic-detail.p-0 > h2').text
    sub_path = os.path.join(parent_path, sub_title)
    if not os.path.exists(sub_path):
        os.makedirs(sub_path)
    for script in sub_soup.find_all('script'):
        if 'img_data' in script.text:
            img_data = re.search(r'.*\'(.*)\'.*', script.text).group(1)
            img_data_list = json.loads(base64.b64decode(img_data).decode('utf-8'))
            threads = []
            for i, img_detail in enumerate(img_data_list):
                img_url = img_base_url + img_detail['img']
                img_path = os.path.join(sub_path, '{:03}'.format(img_detail['p']) + "_" + img_detail['img'])
                print(img_url)
                if not os.path.exists(img_path):
                    t = threading.Thread(target=download_and_check_integrity,
                                         args=(img_url, img_path))
                    t.start()
                    time.sleep(0.1)
                    threads.append(t)
            for t in threads:
                t.join()
            break


def download_chapter_from_link():
    pass


def download_and_check_integrity(download_url, target_path):
    r = requests.get(download_url, headers=headers, stream=True)
    download_counter = 0
    while download_counter < 5:
        with open(target_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        if int(r.headers['Content-Length']) == os.path.getsize(target_path):
            return
    os.remove(target_path)
    print('download failed: url: %s, path: %s' % (download_url, target_path))


argv_iter = iter(sys.argv)
next(argv_iter)
try:
    url = next(argv_iter)
except:
    print("please enter url!")
    exit(1)

if not url.startswith(base_url):
    print("invalid url")
    exit(1)

soup = BeautifulSoup(
    request.urlopen(request.Request(url=url, headers=request_head)).read(), 'html.parser')
try:
    current_dir = os.path.join(
        next(argv_iter), soup.select_one('.comic-info .comic-title').text)
except:
    current_dir = os.path.join(
        os.getcwd(), soup.select_one('.comic-info .comic-title').text)
print(current_dir)

tab_names = soup.select('#myTab span')
tab_panes = soup.select('.tab-content .tab-pane .links-of-books')
if len(tab_names) != len(tab_panes):
    print("program wrong!")
    exit(1)
for count, tab_name in enumerate(tab_names):
    path = os.path.join(current_dir, tab_name.text)
    if not os.path.exists(path):
        os.makedirs(path)
    print(tab_name.text)
    for child in tab_panes[count].descendants:
        if child.name == 'a':
            download_book_from_link(child['href'], path)
