import os
import sys
import unittest
from functools import partial
import subprocess
import time

hdr = {"User-Agent":"Mozilla/5.0"}

def hello(*args):
    print('hello: {} {}'.format(args[0], args[1]))


class TestVinanti(unittest.TestCase):
    
    def test_crawl(self):
        vnt = Vinanti(block=False, backend='aiohttp', old_method=False, max_requests=5,
                      hdrs=hdr, session=True, onfinished=hello, loop_forever=False, wait=0.2)
        url = 'https://docs.python.org/3/reference/index.html'
        vnt.crawl(url)
        
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
