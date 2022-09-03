# www.manhuadb.com漫画下载

# https://www.manhuadb.com/manhua/139

from urllib import request
from bs4 import BeautifulSoup
import os
import re
import base64
import json
import time
import threading
import sys

request_head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'}
base_url = "https://www.manhuadb.com"
opener = request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
request.install_opener(opener)


def download_book_from_link(link: str, parent_path: str):
    print(link, parent_path)
    sub_url = base_url + link
    img_base_url = ('https://i1.manhuadb.com/ccbaike' +
                    link).replace('_', '/').replace('.html', '/')
    img_base_url = re.sub(r'/manhua/[^\/]*', '', img_base_url)
    sub_soup = BeautifulSoup(request.urlopen(request.Request(
        url=sub_url, headers=request_head)).read(), 'html.parser')
    sub_title = sub_soup.select_one(
        'body > div.container-fluid.comic-detail.p-0 > h2').text
    sub_path = os.path.join(parent_path, sub_title)
    if not os.path.exists(sub_path):
        os.makedirs(sub_path)
    for script in sub_soup.find_all('script'):
        if 'img_data' in script.text:
            script_text = script.text
            img_data = re.search(r'.*\'(.*)\'.*', str(script)).group(1)
            img_data_list = json.loads(
                base64.b64decode(img_data).decode('utf-8'))
            for i, img_detail in enumerate(img_data_list):
                img_url = img_base_url + img_detail['img']
                img_path = os.path.join(sub_path, '{:03}'.format(
                    img_detail['p']) + "_" + img_detail['img'])
                print(img_url)
                threads = []
                if not os.path.exists(img_path):
                    t = threading.Thread(target=request.urlretrieve,
                                         args=(img_url, img_path))
                    threads.append(t)
                    t.start()
                    # request.urlretrieve(
                    #     img_base_url + img_detail['img'], img_path)
                    time.sleep(0.02)
                for t in threads:
                    t.join()
            break


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
current_dir = os.path.join(
    os.getcwd(), soup.select_one('.comic-info .comic-title').text)

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
