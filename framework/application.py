
from quopri import decodestring

from framework.requests import Get, Post


def not_found_404_view(request):

    return '404 WHAT', '404 PAGE Not Found'


def decode_value(data):
    decoded_data = {}
    for k, v in data.items():
        val = bytes(v.replace("%", "=").replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val).decode('UTF-8')
        decoded_data[k] = val_decode_str
    return decoded_data


class Application:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):

        request = {}
        path = environ['PATH_INFO']
        if not str(path).endswith('/'):
            path += '/'

        method = environ['REQUEST_METHOD']
        request['method'] = method
        request['path'] = path

        if method == 'GET':
            request_params = Get().get_request_params(environ)
            request['request_params'] = request_params
            print(f'GET-запрос параметры url строки:{request_params}')

        if method == 'POST':
            data = decode_value(Post().get_input_data(environ))
            request['data'] = data
            print(f'POST-запрос, данные из тела запроса:{data}')

        if path in self.routes:
            view = self.routes[path]
        else:
            view = not_found_404_view


        # front controller
        for front in self.fronts:
            front(request)

        # page controller
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


# Новый вид WSGI-application.
# Первый — логирующий (такой же, как основной,
# только для каждого запроса выводит информацию
# (тип запроса и параметры) в консоль.
class DebugApplication(Application):

    def __init__(self, routes_obj, fronts_obj):
        self.application = Application(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


# Новый вид WSGI-application.
# Второй — фейковый (на все запросы пользователя отвечает:
# 200 OK, Hello from Fake).
class FakeApplication(Application):

    def __init__(self, routes_obj, fronts_obj):
        self.application = Application(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']


