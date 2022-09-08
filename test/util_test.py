import unittest
import util
import os


class UtilTest(unittest.TestCase):
    def test_download(self):
        img_path = 'check_integrity.jpg'
        util.download_and_check_integrity('https://i1.manhuadb.com/ccbaike/9/7969/15_qdjtamgq.jpg', img_path)
        self.assert_(os.path.exists(img_path))
        os.remove(img_path)

    def test_img_url_assemble(self):
        chapter_url = 'https://www.manhuadb.com/manhua/118/1090_10917.html'
        img_detail_key = '13_hnkkphwe.jpg'
        img_url = 'https://i1.manhuadb.com/ccbaike/1090/10917/13_hnkkphwe.jpg'
        self.assertEqual(util.img_url_assemble(chapter_url, img_detail_key), img_url)
