import os
import sys
import unittest
from functools import partial

hdr = {"User-Agent":"Mozilla/5.0"}
    

class TestVinanti(unittest.TestCase):
    
    def test_no_async(self):
        vnt = Vinanti(block=True, hdrs=hdr)
        req = vnt.get('http://www.google.com')
        print(req.info)
        req = vnt.post('http://httpbin.org/post', data={'hello':'world'})
        print(req.html)
        req = vnt.get('http://www.wikipedia.org')
        print(req.info)
        req = vnt.get('http://httpbin.org/get', method='HEAD')
        print(req.info)
        
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
