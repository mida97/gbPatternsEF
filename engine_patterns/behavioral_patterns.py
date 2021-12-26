from jsonpickle import dumps, loads

from engine_patterns.view_helper import TabSet
from framework.templator import render


# поведенческий паттерн - наблюдатель
class Observer:

    def update(self, subject, msg):
        pass


class Subject:

    def __init__(self, attrs):
        self.observers = []

    def notify(self, msg):
        for item in self.observers:
            item.update(self, msg)


class SmsNotifier(Observer):

    def update(self, subject, msg):
        for sendto in subject:
            print('SMS->',  msg, ' отправлено пользователю: ', sendto.name)


class EmailNotifier(Observer):

    def update(self, subject, msg):
        for sendto in subject:
            print('EMAIL->', msg, ' отправлено пользователю: ', sendto.name)


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


# поведенческий паттерн - Шаблонный метод
class TemplateView:
    template_name = 'template.html'
    tabs_desc = [[]]
    tab_num = 0

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def get_request_params(self):
        try:
            return self.request_params
        except Exception:
            return {}

    def set_request_params(self, request):
        self.request_params = {}
        if 'request_params' in request:
            self.request_params = request['request_params']

    def render_template_with_context(self):
        context = self.get_context_data()
        tab_set = TabSet(self.tabs_desc)
        currenttab = tab_set.get_tab(self.tab_num),
        template_name = self.get_template()
        context['tabs'] = tab_set.get_tabs()
        context['currenttab'] = currenttab

        if hasattr(self, 'error') and self.error and self.error != "":
            context['error'] = self.error
            return '200 OK', render('error.html', **context)

        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        self.error = None
        self.set_request_params(request)
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class FormView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']


    def save_data(self, data):
        pass

    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            self.set_request_params(request)
            data = self.get_request_data(request)
            self.save_data(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)


# поведенческий паттерн - Стратегия
class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:

    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')

