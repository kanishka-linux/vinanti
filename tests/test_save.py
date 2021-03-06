import os
import sys
import unittest
from functools import partial

def hello(*args):
    result = args[-1]
    if len(args) > 3:
        new_args = args[:-3]
        print(new_args)
    if result:
        info = result.info
        if info:
            content_type = info['content-type']
        else:
            content_type = 'Not Available'
        print('{} {} {} {} error={} cookies={} out-file={}'.format(
                result.url, result.status, content_type,
                result.method, result.error, result.session_cookies,
                result.html
                )
            )


class TestVinanti(unittest.TestCase):
    
    hdr = {"User-Agent":"Mozilla/5.0"}
    
    def test_save_file(self):
        vnt = Vinanti(block=False)
        vnt.get('http://www.google.com',onfinished=hello, hdrs=self.hdr, out='/tmp/1.html')
        vnt.get('http://www.wikipedia.org',onfinished=hello, hdrs=self.hdr, out='/tmp/2.html')
        vnt.get('http://www.google.com',onfinished=hello, hdrs=self.hdr, out='/tmp/3.html')
        
    def test_save_file_aio(self):
        vnt = Vinanti(block=False, backend='aiohttp')
        vnt.get('http://www.google.com',onfinished=hello, hdrs=self.hdr, out='/tmp/1_aio.html')
        vnt.get('http://www.wikipedia.org',onfinished=hello, hdrs=self.hdr, out='/tmp/2_aio.html')
        vnt.get('http://www.google.com',onfinished=hello, hdrs=self.hdr, out='/tmp/3_aio.html')

        
if __name__ == '__main__':
    BASEDIR, BASEFILE = os.path.split(os.path.abspath(__file__))
    parent_basedir, __ = os.path.split(BASEDIR)
    print(parent_basedir)
    sys.path.insert(0, parent_basedir)
    k_dir = os.path.join(parent_basedir, 'vinanti')
    sys.path.insert(0, k_dir)
    print(k_dir)
    from vinanti import Vinanti
    unittest.main()
