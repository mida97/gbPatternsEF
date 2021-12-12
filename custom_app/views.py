from framework import templator
from framework.data_manager import Data_Object


def index_view(request):
    object_list = [
        {'url': '/admin/', 'name': 'Настройки'},
        {'url': '/books/', 'name': 'Список книг'},
        {'url': '/contactus/', 'name': 'Обратная связь'},
    ]

    response = templator.render('index.html', object_list=object_list)
    return '200 OK', [response]


class AdminView:
    def __call__(self, request):
        print(request)
        if request['userrole'] == 'admin':
            return '200 OK', [b'Welcome to admin console']
        else:
            return '403 Forbidden', [b'You are not authorized to access this page']


class Books:

    def __call__(self, request):
        object_list = [
            {'name': 'Once Upon a Time in Hollywood'},
            {'name': 'Master and Margarita'},
            {'name': 'Find Me'},
            {'name': "Goldfinch"}
        ]

        if 'id' in request['request_params']:
            id = int(request['request_params']['id'])-1
            object = [object_list[id]]
            response = templator.render('list.html', object_list=object)
        else:
            response = templator.render('list.html', object_list=object_list)
        return '200 OK', [response]


class ContactUs:

    def __call__(self, request):
        if request['method'] == 'GET':
            response = templator.render('contact.html')
            return '200 OK', [response]
        elif request['method'] == 'POST':
            message_data = request['data']
            del message_data['contact_submitted']
            new_message = Data_Object("MESSAGE", message_data)

            new_message.save(file_name='message.json')
            return '200 OK', [b'Successfully sent!']
        else:
            response = templator.render('contact.html')
            return '200 OK', [response]