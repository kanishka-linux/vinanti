import os
import sys
import unittest
from functools import partial

def hello(*args):
    result = args[-1]
    if len(args) > 3:
        new_args = args[:-3]
        print(new_args)
    if result:
        info = result.info
        if info:
            content_type = info['content-type']
        else:
            content_type = 'Not Available'
        print('{} {} {} {} error={} cookies={} html={}'.format(
                result.url, result.status, content_type,
                result.method, result.error, result.session_cookies,
                result.html
                )
            )

def namaste(*args):
    result = args[-1]
    print('namaste: {} {} html={}'.format(args[-2], result.method, result.html))
    
class TestVinanti(unittest.TestCase):
    
    hdr = {"User-Agent":"Mozilla/5.0"}
    block = False
    
    def test_session(self):
        vnt = Vinanti(block=self.block, method='GET', onfinished=hello, hdrs=self.hdr, group_task=True)
        vnt.get('http://www.google.com', out='/tmp/1.html')
        vnt.add('http://www.wikipedia.org', out='/tmp/2.html')
        vnt.add('http://www.google.com', out='/tmp/3.html')
        vnt.start()

    def test_session_mix(self):
        data_dict = {'hello':'world', 'world':'hello'}
        vnt = Vinanti(block=self.block, onfinished=hello, hdrs=self.hdr, method='POST', data=data_dict, group_task=True)
        vnt.post('http://www.httpbin.org/post')
        vnt.add('http://www.httpbin.org/post', data={'clrs':'algo'})
        vnt.add('http://www.httpbin.org/post', data={'ast':'OS'})
        vnt.add('http://www.httpbin.org/post', data={'tma':'calc'}, hdrs={'user-agent':'curl'})
        vnt.add('http://www.httpbin.org/get', method='GET', params={'hp':'ca', 'ahu':'tfcs'})
        vnt.add('http://httpbin.org/get', method='HEAD', onfinished=namaste)
        vnt.add('http://httpbin.org/ip', method='GET', onfinished=namaste)
        vnt.start()
    
    def test_session_aio(self):
        vnt = Vinanti(block=self.block, method='GET', onfinished=hello, hdrs=self.hdr, group_task=True, backend='aiohttp')
        vnt.get('http://www.google.com', out='/tmp/1.html')
        vnt.add('http://www.wikipedia.org', out='/tmp/2.html')
        vnt.add('http://www.google.com', out='/tmp/3.html')
        vnt.start()

    def test_session_mix_aio(self):
        data_dict = {'hello':'world', 'world':'hello'}
        vnt = Vinanti(block=self.block, onfinished=hello, hdrs=self.hdr, method='POST', data=data_dict, group_task=True, backend='aiohttp')
        vnt.post('http://www.httpbin.org/post')
        vnt.add('http://www.httpbin.org/post', data={'clrs':'algo'})
        vnt.add('http://www.httpbin.org/post', data={'ast':'OS'})
        vnt.add('http://www.httpbin.org/post', data={'tma':'calc'}, hdrs={'user-agent':'curl'})
        vnt.add('http://www.httpbin.org/get', method='GET', params={'hp':'ca', 'ahu':'tfcs'})
        vnt.add('http://httpbin.org/get', method='HEAD', onfinished=namaste)
        vnt.add('http://httpbin.org/ip', method='GET', onfinished=namaste)
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
