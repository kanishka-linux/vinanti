import os
import sys
import unittest
from functools import partial

hdr = {"User-Agent":"Mozilla/5.0"}

def hello(*args):
    print('hello: {}'.format(args[-2]))
    r = args[-1]
    print(r.html)
    print(r.error)
    
logval = False

url1 = 'https://httpbin.org/basic-auth/user-basic/password-basic'
url2 = 'https://httpbin.org/digest-auth/auth/user-digest/password-digest'

class TestVinanti(unittest.TestCase):

    def test_auth_noblock(self):
        vnt = Vinanti(block=False, log=logval, group_task=True)
        vnt.get(url1, onfinished=hello, hdrs=hdr, auth=('user-basic','password-basic'))
        vnt.add(url2, onfinished=hello, hdrs=hdr, auth_digest=('user-digest','password-digest'))
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
