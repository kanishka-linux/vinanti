# Vinanti

Async http request library for python with focus on simplicity


### Installation

        Requires Python 3.5+, No other dependency
        
        ----------------------------------------------------
		$ git clone https://github.com/kanishka-linux/vinanti
		$ cd vinanti
		$ python3 setup.py sdist (or python setup.py sdist)
		$ cd dist
		$ (sudo) pip3 install pkg_available_in_directory (or pip install pkg_available_in_directory) 
        {where 'pkg_available_in_directory' is the exact name of the package created in the 'dist' folder}
        ----------------------------------------------------
        OR
        ----------------------------------------------------
        $ (sudo) pip install git+https://github.com/kanishka-linux/vinanti.git
        ----------------------------------------------------
        use 'sudo' depending on whether you want to install package system-wide or not
			
### Uninstall
		
		$ sudo pip3 uninstall vinanti (OR pip uninstall vinanti)
		

### Let's Discuss some code:

        from vinanti import Vinanti
        
        hdr = {"User-Agent":"Mozilla/5.0"}
        urls = [
            'http://www.yahoo.com',
            'http://www.google.com',
            'http://www.duckduckgo.com',
            'http://www.yahoo.com',
            'http://en.wikipedia.org'
            ]
            
        vnt = Vinanti(block=True)
        
        vnt.get(urls, onfinished=hello, hdrs=hdr)
        vnt.start()
        
        print('Completed')
        
* In above sample code, once vnt.start() gets executed, the main thread will be blocked, but list of urls will be fetched asynchronously. After fetching every url, the **hello** callback function will be called. Once all urls are fetched, it will print 'Completed'.
    
* Now just replace **Vinanti(block=True)** with **Vinanti(block=False)**, in above code and run. It will execute entire code and won't block after vnt.start(). In above code, users will find that it will print 'Completed' immediately, and fetching of urls will keep on going in the background asynchronously.
    
* About Callback **hello** function: This function will be called after fetching of every url has been completed. If no parameters are passed to hello function using partial, then callback will return with three parameters. Signature of default hello function looks like below:
        
        hello(int task_number, str url_name, future_object_with_information)
        
* users can also use: hello(*args) signature, in case arbitrary number of parameters have been passed to hello. In this case, args[-1] will be future_object_with_information, args[-2] will be url_name and args[-3] will be task_number, and rest of parameters will be available in args[0] to onwards.
    
* About future_object_with_information: lets call it future. Result of future is available in future.result()
    
* Accessing information from future_object: Consider following sample hello callback function:
        
        def hello(*args):
            future = args[-1]
            url_submitted = args[-2]
            task_number = args[-3] # Sequential number of url in url_list
            
            result = future.result()
            
            html = result.html #text/html content of fetched url 
            method = result.method #GET,POST, HEAD
            error = result.error #Error information if fetching failed
            url = result.url #Final url location which is fetched
            status_code = result.status #Status code
            cookies = result.session_cookies #If available
            
            header_info = result.info # Dictionary of header information
            content_type = header_info['content-type'] 
            content_length = header_info['content-length']
            #check header_info for more details
    
* If users want different callback function with different parameters for every url. Then they should use vnt.add() after every vnt.get(). See following sample code:
    
        hdr = {"User-Agent":"Mozilla/5.0"}
        vnt = Vinanti(block=True)
        vnt.get('http://www.google.com',onfinished=hello, hdrs=hdr)
        vnt.add('http://www.wikipedia.org',onfinished=namaste, hdrs=hdr)
        vnt.add('http://www.duckduckgo.com',onfinished=konichiwa, hdrs=hdr)
        vnt.start()

### Sample API Usage

* Initiliaze: 
        
        vnt = Vinanti(block=True/False)
        
        Note: Parameters passed during initialization will be shared with all following requests
        
        Eg. if header value is set during initialization then rest of the requests will
        
        share the same header, unless it is overridden by a particular request.

* GET: 
        
        vnt.get(url, onfinished=callback, hdrs=header_dict)

* POST: 
        
        vnt.post(url, onfinished=callback, hdrs=header_dict)

* HEAD: 
        
        vnt.head(url, onfinished=callback, hdrs=header_dict)

* Note: url in above methods can be single http url or list of urls

* ADD:  
        
        vnt.add(url, onfinished=callback, method=method, hdr=header_dict)
        
        Append url with given method to list of tasks. 
        
        Here url should not be list. It should be proper string url.
        
        Method also needs to be specified eg GET, POST or HEAD. 
        
        Default method is GET.
        
* Similar api is for PUT, DELETE, PATCH and OPTIONS
        
* START Fetching: 
        
        vnt.start()

* Some other parameters which can be passed to get, post, head and add functions:

        * params = {key: value} #use with GET
        
        * data = {key: value} or ((key, value1), (key, value2)) #use with POST
        
        * wait = In seconds #wait for seconds before making request
        
        * timeout = In seconds
        
        * out = output-file #save output to this file
        
        * proxies = {type: proxy_server}
        
        * files = files to upload #use with POST
        
        eg. files = '/tmp/file1.txt' OR ('/tmp/file1.txt', '/tmp/file2.txt') 
        
                    OR {'file1': '/tmp/file1.txt', 'file2': '/tmp/file2.txt'}
        
        * auth = ('user', 'passwd') #http basic auth
        
        * auth_digest = ('user', 'passwd') #http digest auth
        
        Examples:
        
        1. vnt = Vinanti(block=False, hdrs={'User-Agent':'Mozilla/5.0'}, onfinished=hello)
        
            # Initialize vinanti in non-blocking mode along with default user-agent string
             
             and same callback function hello for all requests.
             
        2. vnt.get('http://httpbin.org/get', params={'hello':'world'})
        
            # Send request 'http://httpbin.org/get?hello=world'
            
        3. vnt.post('http://httpbin.org/post', data={'world':'hello'}, files='/tmp/file1.txt')
        
            # It will make POST request along with data and files in the body.
            
        4. vnt.get('https://www.duckduckgo.com', out='/tmp/file.html')
        
            # Make request to duckduckgo and save response in /tmp/file.html
            
            # Same kind of request for saving any arbitrary binary file
            
        5. vnt.get('https://www.duckduckgo.com', wait=1.0)
        
            # Wait for 1 second before making this request
            
        5. vnt.get('https://www.duckduckgo.com', timeout=4.0)
        
            # set timeout for above request
            
        6. vnt.get('http://www.httpbin.org/ip', proxies={'http':'http://192.168.2.100:9000'})
        
            # Use proxy for making request
            
        7. vnt.get('https://httpbin.org/basic-auth/user/password', auth=('user','password'))
        
            # http basic authentication
            
        8. vnt.get('https://httpbin.org/digest-auth/auth/usr/passwd', auth_digest=('usr','passwd'))
            
            # http digest authentication
            
        9. vnt.start() # Start fetching
        
* **Troubleshooting:**

        Right way of making concurrent http requests:
    
        1. vnt = Vinanti(block=False, onfinished=hello)
        
        2. vnt.get(url1)
        
        3. vnt.add(url2, method='GET')
        
        4. vnt.add(url3, method='POST', data={'hello':'world'})
        
        5. vnt.add(url4, method='GET')
        
        6. vnt.start()
        ------------------------------------------------------
        
        Wrong way of making concurrent http requests:
    
        1. vnt = Vinanti(block=False, onfinished=hello)
        
        2. vnt.get(url1)
        
        3. vnt.get(url2)
        
        4. vnt.post(url3, data{'hello':'world'})
        
        5. vnt.get(url5) # Only this url will be fetched in this session
        
        6. vnt.start()
        
        In above wrong way, only last request (i.e. that of url5) will be fetched.
        
        Users have to use **vnt.add** to add more http requests to the session,
        
        otherwise only last http request will be fetched.
        -----------------------------------------------------
        
        Another wrong way of starting two concurrent fetch sessions:
        
        1. vnt = Vinanti(block=False, onfinished=hello, method='GET')
        
        2. vnt.get(url1)
        
        3. vnt.add(url2)
        
        4. vnt.start()
        
        5. vnt.add(url3)
        
        6. vnt.add(url4)
        
        7. vnt.start()
        
        In above code lines 2-4 form one fetch session and lines 5-7 form another session.
        
        Starting fetch session from vnt.add won't clear previous sessions list of urls.
        
        Therefore, instruction no. 5 will fetch urls from url1 to url3 and 
        
        instruction no.6 will fetch urls from url1 to url4 again.
        
        Therefore, every fetch session should start with either 
        
        vnt.get, vnt.post, vnt.head, vnt.put, vnt.delete, vnt.patch or vnt.options.
        
        Fetch session should never start with vnt.add
        -----------------------------------------------------
        
* Check [tests](https://github.com/kanishka-linux/vinanti/tree/master/tests) folder, to know more about api usage.

### Some more fun

This library has been mainly made for asynchronous http requests, but the same design allows executing arbitrary functions asynchronously in the background. Instead of passing urls, users just have to pass functions, which will be executed in async manner. In order to pass functions instead of urls, developers have to use api in following manner

        vnt = Vinanti(block=False/True) # Other parameters can be passed during initialization
                    
                                         but they won't be of any use in this case
        
        vnt.function(hello_world, onfinished=hello, rest parameters to hello_world)
        
        vnt.function_add(hello_world, onfinished=hello, rest parameters to hello_world)
        
        vnt.start()
        
        For more details take a look at test_function file in tests folder.
        
        Note: vnt.function and vnt.function_add should not be mixed with http requests session.
        
        i.e. http request session should be separate from above function session
        

### Finally regular synchronous http requests

Just initialize vinanti with block=None, and perform regular http requests. Sample code is given below. 

        vnt = Vinanti(block=None, hdrs=hdr_dict)
        
        req = vnt.get(url)
        
        Now extract information from response object req as below:
        
        html = req.html
        hdr_info = req.info
        status_code = req.status
        error = req.error
        method = req.method
        url = req.url
        cookies = req.session_cookies
        

### Sample application using Vinanti

A sample application using Vinati is available [here](https://github.com/kanishka-linux/WebComics). It is PyQt application. In qt based applications, fetching urls on one hand and keeping GUI responsive on the other hand is bit cumbersome. In order to keep qt gui responsive, one needs to spin thread (for fetching urls) and then GUI needs to be updated using signal/slot mechanism. The application tries do similar thing using Vinanti, but without external threads and signal/slot mechanism. It intializes Vinanti with **block=False**, and tries to achieve same thing using callback mechanism.
    
### Motivation for writing the library

Async/await is a great feature of python, but at the same time pretty confusing. Sprinkling async/await keywords all over code just for making simple url requests seems too much, and can make the code difficult to understand at times. So, I was thinking of async http request library in which developers don't have to write keywords like async/await, event_loop etc.., if they just want to make simple url requests and that too in mostly synchronous code. So accordingly, this library has been designed with as simple api as possible, with everything about content will be handled by callback function.

### About word Vinanti

It means **Request**, in [Marathi](https://en.wikipedia.org/wiki/Marathi_language).
