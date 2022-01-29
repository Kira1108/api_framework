from inspect import Attribute
from urllib import response
import pytest

def test_basic_route_adding(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "Some algorhthm"
        
def test_overlap_throw_exception(api):
    
    @api.route("/home")
    def home(req, resp):
        resp.text = "Some algorhthm"
        
    with pytest.raises(AssertionError):
        @api.route('/home')
        def home2(req, resp):
            resp.text = "Some other algorihm"
            
def test_bumbo_test_session_can_send_requests(api, client):
    RESPONSE_TEXT = "THIS IS COOL"
    
    @api.route("/hey")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT
        
    assert client.get("http://testserver/hey").text == RESPONSE_TEXT
    
    
def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"Hey {name}"
    
    assert client.get("http://testserver/wanghuan").text == "Hey wanghuan"
    
    
def test_default_404_response(api, client):
    response = client.get("http://testserver/notexistsendpoint")
    assert response.status_code == 404
    assert response.text == "Not Found."
    
def test_class_based_handler_get(api, client):
    response_text = "This is a get request"
    @api.route('/book')
    class BookResource:
        def get(self,req, resp):
            resp.text = response_text
            
    assert client.get("http://testserver/book").text == response_text
    
def test_class_based_handler_post(api, client):
    response_text ="This is a post request"
    @api.route('/book')
    class BookResource:
        def post(self, req, resp):
            resp.text = response_text
    assert client.post("http://testserver/book").text ==  response_text
    
    
def test_class_based_method_not_allowed(api, client):
    response_text ="This is a post request"
    @api.route('/book')
    class BookResource:
        def post(self, req, resp):
            resp.text = response_text
            
            
    with pytest.raises(AssertionError):
        client.get("http://testserver/book")
            
            


