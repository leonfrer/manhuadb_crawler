import base64
import json
import os
import re
import threading
import time
from urllib import request

from bs4 import BeautifulSoup

import util

request_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'}
base_url = "https://www.manhuadb.com"


def download_book_from_link(book_url: str, parent_path: str):

    if not re.match(r'^https://www.manhuadb.com/manhua/\d+/[\d_]+\.html$', book_url):
        raise ValueError('wrong url for book!')

    print(book_url, parent_path)
    sub_soup = BeautifulSoup(request.urlopen(request.Request(url=book_url, headers=request_headers)).read(), 'html.parser')
    sub_title = sub_soup.select_one('body > div.container-fluid.comic-detail.p-0 > h2').text
    sub_path = os.path.join(parent_path, sub_title)
    if not os.path.exists(sub_path):
        os.makedirs(sub_path)
    for script in sub_soup.find_all('script'):
        if 'img_data' in script.text:
            img_data = re.search(r'.*\'(.*)\'.+', script.text).group(1)
            img_data_list = json.loads(base64.b64decode(img_data).decode('utf-8'))
            threads = []
            for i, img_detail in enumerate(img_data_list):
                img_url = util.img_url_assemble(book_url, img_detail['img'])
                img_path = os.path.join(sub_path, '{:03}'.format(img_detail['p']) + "_" + img_detail['img'])
                print(img_url)
                if not os.path.exists(img_path):
                    t = threading.Thread(target=util.download_and_check_integrity,
                                         args=(img_url, img_path))
                    t.start()
                    time.sleep(0.5)
                    threads.append(t)
            for t in threads:
                t.join()
            break


def download_series(url: str, store_path: str):

    if not re.match(r'^https://www.manhuadb.com/manhua/\d+/?$', url):
        raise ValueError('wrong url for series!')

    soup = BeautifulSoup(request.urlopen(request.Request(url=url, headers=request_headers)).read(), 'html.parser')
    current_dir = os.path.join(store_path, soup.select_one('.comic-info .comic-title').text)
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
                download_book_from_link(base_url + child['href'], path)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='This is the tool to offline from manhuadb.com',
    )

    parser.add_argument('-t', '--type', nargs=1, choices=['series', 'book'], required=True)
    parser.add_argument('-u', '--url', nargs=1, required=True)
    parser.add_argument('-p', '--path', nargs=1, default=[os.getcwd()])

    args = parser.parse_args()

    if args.type[0] == 'series':
        download_series(args.url[0], args.path[0])
    elif args.type[0] == 'book':
        download_book_from_link(args.url[0], args.path[0])


