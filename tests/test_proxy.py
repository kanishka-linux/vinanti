import os
import sys
import unittest
from functools import partial

hdr = {"User-Agent":"Mozilla/5.0"}

def hello(*args):
    print('hello: {}'.format(args[-2]))
    r = args[-1].result()
    print(r.html)
    print(r.info)

logval = False
proxies = {'http': 'http://192.168.2.10:9000/'}

class TestVinanti(unittest.TestCase):
    
    def test_proxy_block(self):
        vnt = Vinanti(block=True, log=logval, group_task=True)
        vnt.get('http://www.httpbin.org/ip',onfinished=hello, hdrs=hdr, proxies=proxies)
        vnt.add('http://www.httpbin.org/post', method='POST', data={'moe':'curly'}, onfinished=hello, hdrs=hdr, proxies=proxies)
        vnt.start()

    def test_proxy_noblock(self):
        vnt = Vinanti(block=False, log=logval, group_task=True)
        vnt.get('http://www.httpbin.org/ip',onfinished=hello, hdrs=hdr, proxies=proxies)
        vnt.add('http://www.httpbin.org/post', method='POST', data={'moe':'curly'}, onfinished=hello, hdrs=hdr, proxies=proxies)
        vnt.start()
    
        
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
