
from webob import Request, Response
from parse import parse
import inspect

from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

# This is the first version
# the object of this class is callable
# that safisfy PEP 8888 application standard.
# class APISimple:
#     # this is enough for a extremly simple api to work
#     # if you only want to return hellow world oh fuck to the client.
#     def __call__(self, environ, start_response):
#         response_body = b'Hello World Oh Fuck'
#         status = '200 OK'
#         start_response(status, headers = [])
#         return iter([response_body])


class API:
    """User request, and response from webob to create the application.
       API use request to make a response
    """
    
    def __init__(self):
        self.routes = {}
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)
    
    
    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
            
        return None, None
    
    
    def handle_request(self, request):
        """The handler function changes the reponse object inplace"""
        response = Response()
        
        handler, kwargs = self.find_handler(request.path)

        if handler is not None:
            
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AssertionError("Method not allowed", request.method)

            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response    
        
    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found."
    
    # route method is called return wrapper function
    # wrapper takes handler function and return the handler function untouched
    # and add it to API object itself.
    def route(self, path):
    
        def wrapper(handler):
            self.add_route(path, handler)
            return handler
        return wrapper
    
    def add_route(self, path, handler):
        assert path not in self.routes, "Such route already exists"
        self.routes[path] = handler
    
    def test_session(self, base_url = "http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter = RequestsWSGIAdapter(self))
        return session
    