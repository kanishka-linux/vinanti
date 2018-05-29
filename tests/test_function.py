import os
import sys
import unittest
from functools import partial
import subprocess
import time

hdr = {"User-Agent":"Mozilla/5.0"}

def hello(*args):
    print('hello: {} {}'.format(args[-1], args[0]))

def namaste(*args):
    print('namaste: {} {}'.format(args[-1], args[0]))
    
def konichiwa(*args):
    print('konichiwa: {} {}'.format(args[-1], args[0]))

def hello_world(url):
    cmd = ['curl', '-A', 'Mozilla/5.0', url]
    info = subprocess.check_output(cmd)
    return url

class TestVinanti(unittest.TestCase):
    
    def test_function_non_block(self):
        vnt = Vinanti(block=False, group_task=True)
        vnt.function(hello_world, 'http://www.yahoo.com', onfinished=partial(hello, 'noblock_function'))
        vnt.function_add(hello_world, 'http://www.google.com', onfinished=partial(konichiwa, 'noblock'))
        vnt.function_add(hello_world, 'http://www.wikipedia.org', onfinished=partial(namaste, 'noblock'))
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
