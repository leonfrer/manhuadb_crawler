import os
import re

import requests

img_download_headers = {
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


def download_and_check_integrity(download_url, target_path):
    r = requests.get(download_url, headers=img_download_headers, stream=True)
    download_counter = 0
    while download_counter < 5:
        with open(target_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        if int(r.headers['Content-Length']) == os.path.getsize(target_path):
            return
    os.remove(target_path)
    print('download failed: url: %s, path: %s' % (download_url, target_path))


def img_url_assemble(chapter_url: str, img_detail_key: str) -> str:
    return re.sub(r'//www.manhuadb.com/manhua/[^/]*', '//i1.manhuadb.com/ccbaike', chapter_url)\
        .replace('_', '/').replace('.html', '/') + img_detail_key
