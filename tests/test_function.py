import os
import sys
import unittest
from functools import partial
import subprocess
import time

hdr = {"User-Agent":"Mozilla/5.0"}

def hello(*args):
    print('hello: {} {}'.format(args[-1].result(), args[0]))

def namaste(*args):
    print('namaste: {} {}'.format(args[-1].result(), args[0]))

    
def konichiwa(*args):
    print('konichiwa: {} {}'.format(args[-1].result(), args[0]))

def hello_world(url):
    cmd = ['curl', '-A', 'Mozilla/5.0', url]
    info = subprocess.check_output(cmd)
    return url

class TestVinanti(unittest.TestCase):
    
    def test_function_block(self):
        vnt = Vinanti(block=False)
        vnt.function(hello_world, onfinished=partial(hello, 'noblock_function'), url='http://www.yahoo.com')
        vnt.function_add(hello_world, onfinished=partial(konichiwa, 'noblock_function'), url='http://www.google.com')
        vnt.function_add(hello_world, onfinished=partial(namaste, 'noblock_function'), url='http://www.wikipedia.org')
        vnt.start()
        vnt = Vinanti(block=True)
        vnt.function(hello_world, onfinished=partial(hello, 'block_function'), url='http://www.yahoo.com')
        vnt.function_add(hello_world, onfinished=partial(konichiwa, 'block_function'), url='http://www.google.com')
        vnt.function_add(hello_world, onfinished=partial(namaste, 'block_function'), url='http://www.wikipedia.org')
        vnt.start()
        
    def test_function_non_block(self):
        vnt = Vinanti(block=False)
        vnt.function(hello_world, onfinished=partial(hello, 'noblock'), url='http://www.yahoo.com')
        vnt.function_add(hello_world, onfinished=partial(konichiwa, 'noblock'), url='http://www.google.com')
        vnt.function_add(hello_world, onfinished=partial(namaste, 'noblock'), url='http://www.wikipedia.org')
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
