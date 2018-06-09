import os
import sys
import unittest
from functools import partial
import subprocess
import time

hdr = {"User-Agent":"Mozilla/5.0"}

def hello(*args):
    vnt = args[0]
    print('hello: {} {}'.format(args[1], args[2]))
    print(vnt.tasks_count(), vnt.tasks_done(), vnt.tasks_remaining())

def hello_world(*args):
    vnt = args[0]
    print('hello_world: {} {}'.format(args[0], args[1]))

class TestVinanti(unittest.TestCase):
    
    def test_crawl(self):
        vnt = Vinanti(block=False, backend='aiohttp', max_requests=10,
                      hdrs=hdr, session=True, loop_forever=False, wait=0.2)
        url = 'https://docs.python.org/3/reference/index.html'
        vnt.crawl(url, onfinished=partial(hello, vnt))
    
    def test_crawl_urllib(self):
        vnt = Vinanti(block=False, backend='urllib', max_requests=5,
                      hdrs=hdr, session=True, onfinished=hello_world,
                      loop_forever=False, wait=0.2)
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
