from framework import templator
from engine.view_helper import TabSet, Tab
from framework.data_manager import Data_Object

tabs_desc = [
    ['0', '/', 'Главная'],
    ['1', '/another_page/', 'Расписание'],
    ['2', '/contactus/', 'Обратная связь'],
]

tab_set = TabSet(tabs_desc)

def index_view(request):

    response = templator.render('index.html',
                                currenttab=tab_set.get_tab(0),
                                tabs=tab_set.get_tabs())
    return '200 OK', [response]


def another_page(request):

    response = templator.render('another-page.html',
                                date=request.get('date', None),
                                currenttab=tab_set.get_tab(1),
                                tabs=tab_set.get_tabs())
    return '200 OK', [response]


class ContactUs:

    def __call__(self, request):

        if request['method'] == 'POST':
            message_data = request['data']
            del message_data['contact_submitted']
            new_message = Data_Object("MESSAGE", message_data)

            new_message.save(file_name='message.json')

            response = templator.render('contact.html',
                                        success=True,
                                        currenttab=tab_set.get_tab(2),
                                        tabs=tab_set.get_tabs())

            return '200 OK', [response]

        else:
            response = templator.render('contact.html',
                                        success=False,
                                        currenttab=tab_set.get_tab(2),
                                        tabs=tab_set.get_tabs())
            return '200 OK', [response]