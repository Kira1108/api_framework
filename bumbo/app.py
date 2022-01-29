from api import API

app = API()

@app.route("/home")
def home(request, response):
    response.text = "Hello from home page"

@app.route("/about")
def about(request, response):
    response.text = "Hello from about page"
    
@app.route("/")
def ping(request, response):
    response.text = 'Pong'
    
@app.route("/hello/{name}")
def say_hello(request, response, name):
    response.text = f"Hello, {name}, you successfully using named routes."
     
@app.route("/sum/{num1:d}/{num2:d}")
def sum(request, response, num1, num2):
    total = int(num1) + int(num2)
    response.text = f"{num1} + {num2} = {total}"
       
@app.route("/book")
class BookResource:
    def get(self, req, resp):
        resp.text = "Book page of get"
    
    def post(self, req, resp):
        resp.text = "Book page of post"
        

    

    