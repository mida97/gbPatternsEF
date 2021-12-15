from framework import templator
from framework.data_manager import Data_Object


def index_view(request):

    response = templator.render('index.html')
    print(response)
    return '200 OK', [response]


def another_page(request):

    response = templator.render('another-page.html', date=request.get('date', None))
    print(response)
    return '200 OK', [response]



class ContactUs:

    def __call__(self, request):

        if request['method'] == 'POST':
            message_data = request['data']
            del message_data['contact_submitted']
            new_message = Data_Object("MESSAGE", message_data)

            new_message.save(file_name='message.json')

            response = templator.render('contact.html', success=True)
            return '200 OK', [response]

        else:
            response = templator.render('contact.html')
            return '200 OK', [response]