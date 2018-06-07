# Vinanti

Async non-blocking HTTP library for python with focus on simplicity

### Motivation for writing the library

Async/await is an amazing feature of python, but at the same time it is pretty confusing. Sprinkling async/await keywords all over code just for making simple url requests seems too much, and can make the code difficult to understand at times. Besides, trying to use async functionality in a totally synchronous codebase is a recipe for disaster. So, I was thinking of async http request library in which developers don't have to worry about async/await syntax at the api-level.. In the process of exploring this idea, I ended up writing experimental async HTTP client for python (using existing libraries), that doesn't require any knowledge of async/await or even anything related to starting/stopping of event loop at the level of api.

### To whom can this library be useful?

Those who prefer writing synchronous code but need to make asynchronous HTTP requests.

### How async is achieved?

There are two ways, in which async has been achieved in this library.

1. **Using combination of ThreadPool/ProcessPool executor and async/await:** This is the default mode and doesn't require any dependency. Concurrency can be achieved using both threads or processes. It uses python's default urllib.request module for fetching web resources. One can also call this mode as **pseudo async**.

+ In this mode, asyncio's event loop, which also manages scheduling of tasks in this library, executes tasks in the executor [in background](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.run_in_executor). Tasks executed in the executor are not thread safe, therefore care has been taken for maintaining complete separation between request objects passed to them. About callbacks, they are executed once a task completes its execution. Callbacks are the main mechanism through which one receives response object in this library.

+ It is mostly good for small number of async requests. It is default mode, but it can be also activated by setting backend='urllib' while making any request.

2. **Using aiohttp:** Using aiohttp as backend, **real async** can be achieved. Users need to install aiohttp using command:

        $ (sudo) pip/pip3 install aiohttp
        
    and then need to setup backend='aiohttp' during initialization of Vinanti. By using aiohttp as backend, one can easily fire 1000+ requests without breaking a sweat, and all of them will be handled in one sigle thread. Only make sure to keep some time duration between successive requests to same domain using **wait** parameter, in order to not to abuse any web based service.
    

## Features

Featurewise, it is not rich compared to other HTTP clients, at the moment. Its main advantage is, easy to use api which doesn't require knowing anything about async feature of python at the user level. Possibly, it will try to add many other features in future. But currently its main focus is to explore/experiment whether it is possible to build api's to async libraries without users having to deal with async related code/syntax themselves at the api-level or not.

However, Vinanti has **some interesting features** (apart from regular HTTP requests) which are listed below:

+ Allowing both sync/async HTTP requests (default async)

+ Ability to add wait duration between successive requests to same domain, which helps in limiting number of http requests that can be fired at particular domain.

+ Ability to fire list of http requests in async, non-blocking manner.

        urls = [list of 1000 urls]
        
        vnt.get(urls, onfinished=hello)
        
+ Ability to use different http library backends. Currently urllib.request and aiohttp are supported.

+ Better thread safety of callbacks in both the methods.

+ Ability to use either threads or process when backend='urllib'

+ Ability to limit number of concurrent requests at a time.


## Dependencies and Installation
    
### Dependencies

        python 3.5.2+
        
        aiohttp (if backend set to aiohttp)

### Installation
        
        $ git clone https://github.com/kanishka-linux/vinanti
        
        $ cd vinanti
        
        $ python setup.py sdist (or python3 setup.py sdist)
        
        $ cd dist
        
        $ (sudo) pip install pkg_available_in_directory (or pip3 install pkg_available_in_directory) 
        
          # where 'pkg_available_in_directory' is the exact name of the package
          
          # created in the 'dist' folder
          
        
        # OR
        
        
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
        
        # That's it, just good old style nice/clean api
    
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
        
        1. backend = 'urllib' or 'aiohttp' or 'function' (default 'urllib')
        
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
        
        * wait = In seconds # wait for seconds before making request. This
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
        
        * auth_digest = ('user', 'passwd') # http digest auth
                                           # not available for aiohttp
        
        * verify = True/False # If set to False, it will ignore ssl certificate
                              # verification. Useful for self signed certificates.
        
        * binary = True/False # Get html response body in bytes.
        
        * charset = specify character set encoding 
        
        * cookie_unsafe = True/False (default False) # option for aiohttp, in order
                                                     # to enable cookie processing
                                                     # for IP addresses.

        
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
           
           processed at a time. This parameter is handled using asyncio.Semaphore().
           
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
                
        + Use this api depending on need. It is mostly useful, if users want to fire large number of requests with custom callback and other parameters.
        
        + If users don't want to pass different parameters to all requests then do not use group_task and instead simply pass list of urls to request function as given below.
        
                eg. vnt = Vinanti(block=False, group_task=False, max_requests=1000,
                                  backend='aiohttp', --other--params--)
                
                    urls = [list of 1000 urls]
                    
                    vnt.get(urls) 
                    
                    # OR
                    
                    for url in urls:
                    
                        vnt.get(url) 
                    
        
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
        
        vnt = Vinanti(block=False, backend='function')
        
        vnt.function(hello_world, rest parameters to hello_world, onfinished=hello)
        
        for executing function in separate process:
        
        vnt = Vinanti(block=False, backend='function', multiprocess=True)
        
        vnt.function(hello_world, rest parameters to hello_world)
                
        For more details take a look at test_function file in tests folder.
        
        Note: vnt.function and vnt.function_add should not be mixed with http requests session.
        
        i.e. http request session should be separate from above function session
        
        Note: Executing functins in this way is not thread safe, so use with care.
        
              However, callbacks are thread safe.
        
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

+ **Thread Safety of callbacks** : 
    
    1. Do not use two instances of Vinanti in the same application. If you are using two instances, then make sure that they both do not access callbacks with same global/common variable.

    2. As long as you are not accessing same callbacks from different threads (except the main thread in which main application code is running), you don't have to worry about thread safety. But if, you need to access same callbacks from different thread then arrange for callback using following method:

            vnt.loop.call_soon_threadsafe(callback)
        
    3. If above points do not apply and your use case is even more complex then it is better to use traditional synchronization primitives like lock or semaphore.

+ In order to make api simple, the library has accepted some performance penalty especially using aiohttp as backend. It can't reuse aiohttp's connection pool. In order to use aiohttp's default connection pool, vinanti might have to turn entire code into async including its api, which could have defeated its purpose of simple and easy to api. If anyone has solution to it, then they can sure submit pull request without changing api. However, this performance penalty looks negligible (compared to other sync http clients) when used in synchronous code.

## Sample applications using Vinanti

1. A sample application using Vinati is available [here](https://github.com/kanishka-linux/WebComics). It is PyQt application. In qt based applications, fetching urls on one hand and keeping GUI responsive on the other hand is bit cumbersome. In order to keep qt gui responsive, one needs to spin thread (for fetching urls) and then GUI needs to be updated using signal/slot mechanism. The application tries do similar thing using Vinanti, but without external threads and signal/slot mechanism. It intializes Vinanti with **block=False**, and tries to achieve same thing using callback mechanism.

+ Note: This approach may work for simple pyqt applications. For complicated applications, it is better to use custom signal/slot mechanism along with vinanti.

## Sample library using Vinanti

A sample [tvdb-async](https://github.com/kanishka-linux/tvdb-async) library is also available. This library allows fetching of tv series metadata from thetvdb.com in async manner as it is made available.

## About word Vinanti

It means **Request**, in [Marathi](https://en.wikipedia.org/wiki/Marathi_language).
