def parse_url_param(params: str):
    result = {}
    if params:
        params = params.split('&')
        for i in params:
            k, v = i.split('=')
            result[k] = v
    return result

class Get:

    @staticmethod
    def get_request_params(env):
        query_string = env['QUERY_STRING']
        request_params = parse_url_param(query_string)
        return request_params  # -> {'id': '1', 'category': '10'}


class Post:

    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            params = data.split('&')
            for i in params:
                k, v = i.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_input_data(env):
        result = {}
        data = b''
        content_length = env.get('CONTENT_LENGTH')
        #print(content_length)
        #читаем данные, полученные от wsgi
        if content_length:
            data = env['wsgi.input'].read(int(content_length))

        if data:
            # декодируем данные
            data_str = data.decode(encoding='utf-8')
            # собираем их в словарь
            result = Post().parse_input_data(data_str)
        return result
