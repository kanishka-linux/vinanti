# Vinanti

Experimental async http request library for python with focus on simplicity

### Installation

		$ git clone https://github.com/kanishka-linux/vinanti
		$ cd vinanti
		$ python3 setup.py sdist (or python setup.py sdist)
		$ cd dist
		$ sudo pip3 install pkg_available_in_directory (or pip install pkg_available_in_directory) 
        {where 'pkg_available_in_directory' is the exact name of the package created in the 'dist' folder}
			
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
        
* Check [tests](https://github.com/kanishka-linux/vinanti/tree/master/tests) folder, to know more about api usage. 

### Sample application using Vinanti

A sample application using Vinati is available [here](https://github.com/kanishka-linux/WebComics/tree/master/WebComics-vinanti). It is PyQt application. In qt based applications, fetching urls on one hand and keeping GUI responsive on the other hand is bit cumbersome. In order to keep qt gui responsive, one needs to spin thread (for fetching urls) and then GUI needs to be updated using signal/slot mechanism. The application tries do similar thing using Vinanti, but without using threads and signal/slot mechanism. It intializes Vinanti with **block=False**, and tries to achieve same thing using callback mechanism.
    
### Motivation for writing the library

Async/await is a great feature of python, but at the same time pretty confusing. Sprinkling async/await keywords all over code just for making simple url requests seems too much, and can make the code difficult to understand at times. So, I was thinking of async http request library in which developers don't have to write keywords like async/await, event_loop etc.., if they just want to make simple url requests and that too in mostly synchronous code. So accordingly, this library has been designed with as simple api as possible, with everything about content will be handled by callback function.

### Caution

This library is highly experimental and currently only supports GET, POST and HEAD requests in limited manner. There is no support for cookies or uploading files at the moment. If program looks stable after thorough testing, only then other advance features will be added to it. It is working fine within small synchronous programs. But, I don't know how it will behave in large complex program. So, for a time being just play with it and don't use it in production till it achieves maturity. 

### About word Vinanti

It means **Request**, in author's [native language](https://en.wikipedia.org/wiki/Marathi_language).
