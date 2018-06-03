import os
import sys
import unittest
from functools import partial

hdr = {"User-Agent":"Mozilla/5.0"}

def hello(*args):
    print('hello: {}'.format(args[-2]))
    r = args[-1]
    print(r.html)
    print(r.info)
    print(r.info['content-type'])

logval = False

class TestVinanti(unittest.TestCase):
    
    path = os.getcwd()
    file1 = os.path.join(path, 'post_file1.txt')
    file2 = os.path.join(path, 'post_file2.txt')
    
    def test_post_file_aio(self):
        vnt = Vinanti(block=False, log=logval, group_task=True, backend='aiohttp')
        file1 = self.file1
        file2 = self.file2
        file_single = file1
        file_tuple = (file1, file2)
        file_dict = {'Title-One':file1, 'Title-Two':file2}
        data_dict = {'hello':'world', 'world':'hello'}
        vnt.post('http://www.httpbin.org/post',onfinished=hello, hdrs=hdr, files=file_single)
        vnt.add('http://www.httpbin.org/post', method='POST', onfinished=hello, hdrs=hdr, files=file_tuple)
        vnt.add('http://www.httpbin.org/post', method='POST', onfinished=hello, hdrs=hdr, files=file_dict)
        vnt.add('http://www.httpbin.org/post', method='POST', onfinished=hello, hdrs=hdr, files=file_single, data=data_dict)
        vnt.start()
    
    def test_post_file_noblock(self):
        vnt = Vinanti(block=False, log=logval, group_task=True, backend='urllib')
        file1 = self.file1
        file2 = self.file2
        file_single = file1
        file_tuple = (file1, file2)
        file_dict = {'Title-One':file1, 'Title-Two':file2}
        data_dict = {'hello':'world', 'world':'hello'}
        vnt.post('http://www.httpbin.org/post',onfinished=hello, hdrs=hdr, files=file_single)
        vnt.add('http://www.httpbin.org/post', method='POST', onfinished=hello, hdrs=hdr, files=file_tuple)
        vnt.add('http://www.httpbin.org/post', method='POST', onfinished=hello, hdrs=hdr, files=file_dict)
        vnt.add('http://www.httpbin.org/post', method='POST', onfinished=hello, hdrs=hdr, files=file_single, data=data_dict)
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
