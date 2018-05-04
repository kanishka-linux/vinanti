import os
import sys
import unittest
from functools import partial

hdr = {"User-Agent":"Mozilla/5.0"}

def hello(*args):
    result = args[-1].result()
    print('hello: {} {}'.format(args[-2], result.method))

def namaste(*args):
    result = args[-1].result()
    print('namaste: {} {}'.format(args[-2], result.method))

    
def konichiwa(*args):
    result = args[-1].result()
    print('konichiwa: {} {}'.format(args[-2], result.method))

def bonjour(*args):
    result = args[-1].result()
    print('bonjour: {} {}'.format(args[-2], result.method))
    print(result.html)
    

class TestVinanti(unittest.TestCase):
    
    def test_add_block(self):
        vnt = Vinanti(block=True)
        vnt.get('http://www.google.com',onfinished=hello, hdrs=hdr)
        vnt.add('http://www.wikipedia.org',onfinished=namaste, hdrs=hdr)
        vnt.add('http://www.duckduckgo.com',onfinished=konichiwa, hdrs=hdr)
        data_post = (('moe', 'curly'), ('moe', 'larry'))
        vnt.add('http://httpbin.org/post', method='POST', onfinished=bonjour, hdrs=hdr, data=data_post)
        vnt.add('http://httpbin.org/get', method='HEAD', onfinished=hello, hdrs=hdr)
        vnt.start()
        
    def test_add_noblock(self):
        vnt = Vinanti(block=False)
        vnt.get('http://www.google.com',onfinished=hello, hdrs=hdr)
        vnt.add('http://www.wikipedia.org',onfinished=namaste, hdrs=hdr)
        vnt.add('http://www.duckduckgo.com',onfinished=konichiwa, hdrs=hdr)
        data_dict = {'Fyodor Dostoyevsky':'Crime and Punishment', 'Shivaji Sawant':'Mrityunjaya'}
        vnt.add('http://httpbin.org/post', method='POST', onfinished=bonjour, hdrs=hdr, data=data_dict)
        vnt.add('http://httpbin.org/get', method='HEAD', onfinished=hello, hdrs=hdr)
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
