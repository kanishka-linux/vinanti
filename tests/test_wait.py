import os
import sys
import unittest
from functools import partial

hdr = {"User-Agent":"Mozilla/5.0"}

def hello(*args):
    print('hello: {}'.format(args[-2]))

def namaste(*args):
    print('namaste: {}'.format(args[-2]))

    
def konichiwa(*args):
    print('konichiwa: {}'.format(args[-2]))


class TestVinanti(unittest.TestCase):
    
    def test_add_noblock(self):
        vnt = Vinanti(block=False, log=False, hdrs=hdr, wait=1.0)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.google.com',onfinished=hello)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.duckduckgo.com',onfinished=konichiwa)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
        vnt.get('http://www.wikipedia.org',onfinished=namaste)
    
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
