import unittest
import requests
import os


class TestCheckIntegrity(unittest.TestCase):
    fetch_link = "https://i1.manhuadb.com/ccbaike/9/7969/15_qdjtamgq.jpg"
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

    def check_download_content_integrity(self):
        r = requests.get(self.fetch_link, headers=self.headers, stream=True)
        pic_path = 'filename.jpg'
        with open(pic_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

        self.assertEqual(int(r.headers['Content-Length']), os.path.getsize(pic_path))


if __name__ == '__main__':
    TestCheckIntegrity.main()
