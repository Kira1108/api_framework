from wsgiref.simple_server import make_server

def application(environ, start_response):
    """
    Args:
        environ (dict): dictionary of environment variables
        start_response (Callable): function that start response

    Returns:
        [str]: list of string [Reponse body]
    """
    response_body = [
        f"{key}: {value}" for key, value in sorted(environ.items())
    ]
    
    response_body = "\n".join(response_body)
    
    status = "200 OK"
    
    response_headers = [
        ("Content-type","text/plain")
    ]
    
    start_response(status, response_headers)
    
    return [response_body.encode('utf-8')]


class Reverseware:
    """Use reverse ware, do some common thing wrapping app."""
    def __init__(self, app):
        self.wrapped_app = app
        
        
    def __call__(self, environ, start_response, *args, **kwargs):
        wrapped_app_response = self.wrapped_app(environ, start_response)
        return [data[::-1] for data in wrapped_app_response]


if __name__ == "__main__":
    # make a server and server an app
    server = make_server('localhost', 8000, app = Reverseware(application))
    server.serve_forever()
    
    

