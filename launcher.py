from wsgiref.simple_server import make_server
from framework.application import application


if __name__ == '__main__':
    with make_server('', 8000, application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()
