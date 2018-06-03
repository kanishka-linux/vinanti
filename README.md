# Vinanti

Async non-blocking HTTP library for python with focus on simplicity

### Motivation for writing the library

Async/await is a great feature of python, but at the same time pretty confusing. Sprinkling async/await keywords all over code just for making simple url requests seems too much, and can make the code difficult to understand at times. So, I was thinking of async http request library in which developers don't have to write keywords like async/await, event_loop etc.., if they just want to make asynchronous url requests and **that too in mostly synchronous code**. So accordingly, this library has been designed with as simple api as possible that doesn't require using any async related keyword at the api-level, and everything about content will be handled by callback function.

### To whom can this library be useful?

Those who prefer writing synchronous code but need to make asynchronous HTTP requests.

### Is there any other advantage?

No. Its only advantage is, easy to use api without knowing anything about async feature of python. Featurewise, it may not be rich compared to other HTTP clients, at the moment, in other areas.
 

### How async is achieved?

1. **Using concurrent.futures:** This is default mode and doesn't require any dependency. Concurrency can be achieved using both threads or processes. It uses python's default urllib.request module for fetching web resources. Good for small number of async requests.

2. **Using aiohttp:** Using aiohttp as backend, real async can be achieved. Users need to install aiohttp using command:

        $ (sudo) pip/pip3 install aiohttp
        
    and then need to setup backend='aiohttp' during initialization of Vinanti.
    
### Dependencies

        python 3.5.2+
        
        aiohttp (if backend set to aiohttp)

### Installation
        
		$ git clone https://github.com/kanishka-linux/vinanti
        
		$ cd vinanti
        
		$ python setup.py sdist (or python3 setup.py sdist)
        
		$ cd dist
        
		$ (sudo) pip install pkg_available_in_directory (or pip3 install pkg_available_in_directory) 
        
          #where 'pkg_available_in_directory' is the exact name of the package
          
          #created in the 'dist' folder
          
        
        OR
        
        
        $ (sudo) pip install git+https://github.com/kanishka-linux/vinanti.git
        
        
**Note:** use 'sudo' depending on whether you want to install package system-wide or not
        
**Note:** use pip or pip3 depending on what is available on your system
			
### Uninstall
		
		$ (sudo) pip uninstall vinanti (OR pip3 uninstall vinanti)
		

## Let's Discuss some code:

        from vinanti import Vinanti
        
        def hello(*args):
            print(args)
        
        hdr = {"User-Agent":"Mozilla/5.0"}
        urls = [
            'http://www.yahoo.com',
            'http://www.google.com',
            'http://www.duckduckgo.com',
            'http://www.yahoo.com',
            'http://en.wikipedia.org'
            ]
            
        vnt = Vinanti(block=False)
        
        vnt.get(urls, onfinished=hello, hdrs=hdr)
        
        print('Completed')
        
        #That's it, just good old style nice/clean api
    
* After running above code, users will find that it will print 'Completed' immediately, and fetching of urls will keep on going in the background asynchronously.
    
* About Callback **hello** function: This function will be called after fetching of every url has been completed. If no parameters are passed to hello function using partial, then callback will return with three parameters. Signature of default hello function looks like below:
        
        hello(int task_number, str url_name, response_object)
        
* users can also use: hello(*args) signature, in case arbitrary number of parameters have been passed to hello. In this case, args[-1] will be response_object, args[-2] will be url_name and args[-3] will be task_number, and rest of parameters will be available in args[0] to onwards.
        
* Accessing information: Consider following sample hello callback function:
        
        def hello(*args):
            result = args[-1] #Response object
            
            url_submitted = args[-2] #Submitted url
            
            task_number = args[-3] #Sequential number of url
            
            if result: # Check if result is available or not
            
                html = result.html #text/html content of fetched url 
                
                method = result.method #GET,POST, HEAD etc..
                
                error = result.error #Error information if fetching failed
                
                url = result.url #Final url location which has been fetched
                
                status_code = result.status #Status code
                
                cookies = result.session_cookies #If available
                
                header_info = result.info #Dictionary of header information
                
                content_type = header_info['content-type'] 
                
                content_length = header_info['content-length']
                
                #check header_info for more details

## Sample API Usage

* Initiliaze: 
        
        vnt = Vinanti(block=True/False)
        
        Note: Parameters passed during initialization will be shared with all following requests
        
        Eg. if header value is set during initialization then rest of the requests will
        
        share the same header, unless it is overridden by a particular request.
        
        Some other important parameters which can be passed during initialization:
        
        1. backend = 'urllib' or 'aiohttp' (default urllib)
        
        2. group_task = True/False (default False)
        
        3. session = True/False (default False) # Maintain session cookies between requests.
                                                # This option will automatically handle setting
                                                # and sending of session cookies similar to
                                                # web browser. Default is False
        
        4. max_requests = maximum concurrent requests (default 10)
        
        5. multiprocess = True/False (default False) # This parameter will allow
                                                     # using separate process
                                                     # for every request.
                                                     # Useful only when backend='urllib'

* GET: 
        
        vnt.get(url, onfinished=callback, hdrs=header_dict)

* POST: 
        
        vnt.post(url, onfinished=callback, hdrs=header_dict)

* HEAD: 
        
        vnt.head(url, onfinished=callback, hdrs=header_dict)

* Note: url in above methods can be single http url or list of urls

* ADD:  

        {only when group_task=True}
        
        vnt.add(url, onfinished=callback, method=method, hdr=header_dict)
        
        Append url with given method to list of tasks. 
        
        Here url should not be list. It should be proper string url.
        
        Method also needs to be specified eg GET, POST or HEAD. 
        
        Default method is GET.
        
* Similar api is for PUT, DELETE, PATCH and OPTIONS

* Some other parameters which can be passed to http request functions or can be used during initialization:
        
        * params = {key: value} #use with GET
        
        * data = {key: value} or ((key, value1), (key, value2)) #use with POST
        
        * wait = In seconds #wait for seconds before making request. This
                            # parameter works domain wise. Applicable from 
                            # second consecutive
                            # request to same domain in the same session.
        
        * timeout = In seconds
        
        * out = output-file #save output to this file
        
        * proxies = {type: proxy_server}
        
        * files = files to upload #use with POST
        
        eg. files = '/tmp/file1.txt' OR ('/tmp/file1.txt', '/tmp/file2.txt') 
        
                    OR {'file1': '/tmp/file1.txt', 'file2': '/tmp/file2.txt'}
        
        * auth = ('user', 'passwd') #http basic auth
        
        * auth_digest = ('user', 'passwd') #http digest auth
        
        * verify = True/False # If set to False, it will ignore ssl certificate
                              # verification. Useful for self signed certificates.
        
        * binary = True/False # Get html response body in bytes.
        
        * charset = specify character set encoding 
        
        Examples:
        
        1. vnt = Vinanti(block=False, hdrs={'User-Agent':'Mozilla/5.0'}, onfinished=hello, max_requests=50)
        
            # Initialize vinanti in non-blocking mode along with default user-agent string
             
             and same callback function hello for all following requests, with maximum limit
             
             of concurrent requests set to 50.
             
        2. vnt.get('http://httpbin.org/get', params={'hello':'world'})
        
            # Send request 'http://httpbin.org/get?hello=world'
            
        3. vnt.post('http://httpbin.org/post', data={'world':'hello'}, files='/tmp/file1.txt')
        
            # It will make POST request along with data and files in the body.
            
        4. vnt.get('https://www.duckduckgo.com', out='/tmp/file.html')
        
            # Make request to duckduckgo and save response in /tmp/file.html
            
            # Same kind of request for saving any arbitrary binary file
            
        5. vnt.get('https://www.duckduckgo.com', wait=1.0)
        
            # Wait for 1 second if this is second request to duckduckgo.com
            
        6. vnt.get('https://www.duckduckgo.com', timeout=4.0)
        
            # set timeout for above request
            
        7. vnt.get('http://www.httpbin.org/ip', proxies={'http':'http://192.168.2.100:9000'})
        
            # Use proxy for making request
            
        8. vnt.get('https://httpbin.org/basic-auth/user/password', auth=('user','password'))
        
            # http basic authentication
            
        9. vnt.get('https://httpbin.org/digest-auth/auth/usr/passwd', auth_digest=('usr','passwd'))
            
            # http digest authentication
            
        10. vnt.start() # Start fetching when group_task=True
        
* Accessing few more properties on running tasks:
        
        1. vnt.tasks_count() # Total tasks count in a session
        
        2. vnt.tasks_done() # Total tasks done
        
        3. vnt.tasks_remaining() # Total tasks remaining
        
        Note: Above properties are approximate.
        
* Clearing Session:

        1. vnt.session_clear() # clear all session cookies 
        
        2. vnt.session_clear(netloc) # clear session cookie from specific domain
        
        Eg. if url is 'https://en.wikipedia.org/wiki/Main_Page' then netloc is
        
        'en.wikipedia.org'. 
        
        vnt.session.clear('en.wikipedia.org'), will clear session cookies related
        
        to wikipedia.
        
        3. vnt.clear() # This will reset everything to default values 
        
* More Explanation on important parameters

    + **session = True/False** 
    
        See following code:
        
            1. vnt = Vinanti(block=False, session=True, hdrs=hdr_dict)
            
            2. vnt.get(url, auth=(user, passwd), onfinished=hello) # Establish session
            
            3. vnt.get(url) # Try to make request to same url without authentication,
                            # but it won't work
                            # Why? It is async code, both instructions 2, 3 will
                            # try to execute concurrently.
                            
        So, what is correct method of using same session?
        
        * First wait for instruction 2 to complete and then execute instruction 3
          and all other subsequent http requests in callback hello function. 
          
          (See test_cookie_session.py file in tests folder for more details)
          
    + **max_requests = 10** (default is 10). 
     
           This parameter specifies maximum number of concurrent requests at a time.
           
           Users can fire any number of requests, but only 10 requests will be 
           
           processed at a time. All other requests will be queued. Once total executing
           
           requests will fall below 10, the first queued item will be removed from waiting queue
           
           and will be added to current executing task list for execution.
           
           Depending on system specification, users can set this max_requests to 
           
           something higher like 20, 30 or even 100+. 
           
           If multiprocess is set to True during initialization then this many number
           
           of processes will be created to manage requests concurrently for urllib
           
           backend.
       
    + **group_task = True/False** (default False)
        
                vnt = Vinanti(block=False, group_task=True, hdrs=hdr_dict,
                              max_requests=100, backend='aiohttp')
                
                url1 = first_url
                
                url2 = second_url
                
                url3 = third_url
                
                vnt.get(url1, onfinished=hello) # First request.
                                                # If group_task would have been
                                                # False then
                                                # fetching of url1 would
                                                # have been started immediately.
                                                
                vnt.add(url2, method='GET', onfinished=new_hello)
                        
                        # Append url2 to group_task with GET method
                        # and different callback
                        
                vnt.add(url3, method='POST', data={'usr':'id'}, onfinshed=hello_world)
                        
                        # Append url3 to group_task with POST method
                        # and different callback
                        
                vnt.start() # Process of fetching will start at this point
                
        + Use this api depending on need. Mostly useful, if users want to fire large number of requests.
        
    + **wait = In seconds** (This parameter works only domainwise.)
    
            This parameter adds some wait duration in seconds between two consecutive requests
            
            to same domain. If this parameter is set during initialization then wait duration will
            
            be set for all subsequent requests domainwise. 
            
            This parameter along with max_requests will throttle maximum requests to same domain.
            
            Developers should use these two parameters carefully and rationally,
            
            in order to not to abuse any web based service.
        
        
* Check [tests](https://github.com/kanishka-linux/vinanti/tree/master/tests) folder, to know more about api usage.

## Some more fun

This library has been mainly made for asynchronous http requests, but the same design allows executing arbitrary functions asynchronously in the background. Instead of passing urls, users just have to pass functions. In order to pass functions instead of urls, developers have to use api in following manner
        
        def hello_world(*args):
            print("hello world")
            
        def hello(*args):
            print("hello")
        
        vnt = Vinanti(block=False/True, group_task=True) # Other parameters can be passed during initialization
                    
                                                        # but they won't work in the case of functions.
        
        vnt.function(hello_world, rest parameters to hello_world, onfinished=hello)
        
        vnt.function_add(hello_world, rest parameters to hello_world, onfinished=hello)
        
        vnt.start()
        
        For more details take a look at test_function file in tests folder.
        
        Note: vnt.function and vnt.function_add should not be mixed with http requests session.
        
        i.e. http request session should be separate from above function session
        
        Note: This feature is unstable, use with care
        
## Finally regular synchronous http requests

Just initialize vinanti with block=True, and perform regular http requests. Sample code is given below. 

        vnt = Vinanti(block=True, hdrs=hdr_dict)
        
        req = vnt.get(url)
        
        Now extract information from response object req as below:
        
        html = req.html
        hdr_info = req.info
        status_code = req.status
        error = req.error
        method = req.method
        url = req.url
        cookies = req.session_cookies

## Some Performance Issues

In order to make api simple, the library has accepted some performance penalty especially using aiohttp as backend. It can't reuse aiohttp's default connection pool. In order to use aiohttp's default connection pool, vinanti might have to use async related keywords at api level, which could have defeated its purpose of simple and easy to api. If anyone has solution to it, then they can sure submit pull request without changing api. However, this performance penalty looks negligible (compared to other sync http clients) when used in synchronous code.

## Sample applications using Vinanti

1. A sample application using Vinati is available [here](https://github.com/kanishka-linux/WebComics). It is PyQt application. In qt based applications, fetching urls on one hand and keeping GUI responsive on the other hand is bit cumbersome. In order to keep qt gui responsive, one needs to spin thread (for fetching urls) and then GUI needs to be updated using signal/slot mechanism. The application tries do similar thing using Vinanti, but without external threads and signal/slot mechanism. It intializes Vinanti with **block=False**, and tries to achieve same thing using callback mechanism.

+ Note: This approach may work for simple pyqt applications. For complicated applications, it is better to use custom signal/slot mechanism along with vinanti.

2. Vinanti has also been used in [this application](https://github.com/kanishka-linux/kawaii-player), in order to manage session between master and slave in pc-to-pc casting mode. In pc-to-pc casting mode, the master computer can send videos to slave computer for playback, which will be then controlled by master. If username and password has been set for slave, along with cookies, then authentication and cookies are managed by vinanti in non-blocking mode.

## Sample library using Vinanti

A sample [tvdb-async](https://github.com/kanishka-linux/tvdb-async) library is also available. This library allows fetching of tv series metadata from thetvdb.com in async manner as it is made available.

## About word Vinanti

It means **Request**, in [Marathi](https://en.wikipedia.org/wiki/Marathi_language).
