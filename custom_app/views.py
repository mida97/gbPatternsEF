from engine_patterns.behavioral_patterns import ListView, FormView, BaseSerializer, EmailNotifier, SmsNotifier
from framework.templator import render
from framework.data_manager import DataForSave
from engine_patterns.logger_singleton import Logger

from engine_patterns.view_helper import TabSet, Tab
from engine_patterns.model_service import ModelService

from engine_patterns.structural_patterns import AppRoute, Debug

#routes наполняется вызовами декоратора @AppRoute при импорте текущего файла
routes = {}

model_service = ModelService()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

tabs = [
    ['0', '/', 'Главная'],
    ['1', '/timetable/', 'Расписание'],
    ['2', '/student-list/', 'Студенты'],
    ['3', '/contactus/', 'Обратная связь'],
]

tab_set = TabSet(tabs)


# контроллер - список категорий
@AppRoute(routes=routes, urls=['/category-list/', '/'])
class CategoryList(ListView):
    template_name = 'category_list.html'
    tabs_desc = tabs
    tab_num = 0
    queryset = model_service.get_all('category')


# контроллер - список курсов
@AppRoute(routes=routes, url='/courses-list/')
class CoursesList(ListView):
    template_name = 'course_list.html'
    tabs_desc = tabs
    tab_num = 0
    def get_context_data(self):
        try:
            category_id = int(super().get_request_params()['id'])
            category = model_service.find_by_id('category', category_id)
            self.queryset = category.courses
            logger.log('Список курсов для категории')
            context = super().get_context_data()
            context['category'] = category
        except KeyError:
            self.queryset = model_service.get_all('course')
            logger.log('Список всех курсов')
            context = super().get_context_data()
        return context


# контроллер - создать курс
@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост

            category = None
            if self.category_id != -1:
                category = model_service.find_by_id('category', int(self.category_id))
                data = request['data']

                description = model_service.decode_value(data['description'])
                name = model_service.decode_value(data['name'])
                course_type = model_service.decode_value(data['type'])

                attrs = {'name': name,
                         'type': course_type,
                         'description': description,
                         'category': category.id}
                new_course = model_service.create('course', attrs)
                category.courses.append(new_course)
                new_course.observers.append(email_notifier)
                new_course.observers.append(sms_notifier)

            return '200 OK', render('course_list.html',
                                    currenttab=tab_set.get_tab(0),
                                    tabs=tab_set.get_tabs(),
                                    category=category,
                                    objects_list=category.courses)
        else:
            try:
                if 'id' not in request['request_params']:
                    return '200 OK', render('error.html',
                                        currenttab=tab_set.get_tab(0),
                                        tabs=tab_set.get_tabs(),
                                        error='Курс можно создать только из категории')

                self.category_id = int(request['request_params']['id'])

                category = model_service.find_by_id('category', int(self.category_id))

                return '200 OK', render('create_course.html',
                                        currenttab=tab_set.get_tab(0),
                                        tabs=tab_set.get_tabs(),
                                        category=category)
            except KeyError:
                return '200 OK', render('error.html',
                                        currenttab=tab_set.get_tab(0),
                                        tabs=tab_set.get_tabs(),
                                        error='Ошибка создания курса')


# контроллер - создать категорию
@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    parent_id = -1

    @Debug(name='CreateCategory')
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост

            data = request['data']

            name = data['name']
            name = model_service.decode_value(name)

            parent = None
            if self.parent_id != -1:
                parent = model_service.find_by_id('category', int(self.parent_id))

            attrs = {'name': name,  'parent': parent}
            new_category = model_service.create('category', attrs)
            if parent:
                parent.children.append(new_category)
            new_category.update_fullname()

            return '200 OK', render('category_list.html',
                                    currenttab=tab_set.get_tab(0),
                                    tabs=tab_set.get_tabs(),
                                    objects_list=model_service.get_all('category'))
        else:
            parent = None
            if 'id' in request['request_params']:
                self.parent_id = int(request['request_params']['id'])
                parent = model_service.find_by_id('category', int(self.parent_id))

            return '200 OK', render('create_category.html',
                                    currenttab=tab_set.get_tab(0),
                                    tabs=tab_set.get_tabs(),
                                    objects_list=model_service.get_all('category'),
                                    parent=parent)


# контроллер - редактировать курс
@AppRoute(routes=routes, url='/edit-course/')
class EditCourse:
    course_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост

            if self.course_id != -1:
                course = model_service.find_by_id('course', int(self.course_id))
                data = request['data']
                attrs = {}
                attrlist = ['name',
                            'type',
                            'description',
                            'course_platform',
                            'course_location'
                            ]
                for attr in attrlist:
                    if attr in dict(data).keys():
                        attrs[attr] = model_service.decode_value(data[attr])

                model_service.edit('course', course.id, attrs)
                category = model_service.find_by_id('category', int(course.category))

                return '200 OK', render('course_list.html',
                                    currenttab=tab_set.get_tab(0),
                                    tabs=tab_set.get_tabs(),
                                    category=category,
                                    objects_list=category.courses)

        else:
            try:
                if not request['request_params']['id']:
                    return '200 OK', render('error.html',
                                        currenttab=tab_set.get_tab(0),
                                        tabs=tab_set.get_tabs(),
                                        error='Ошибка редактирования курса')

                self.course_id = int(request['request_params']['id'])
                course = model_service.find_by_id('course', int(self.course_id))

                return '200 OK', render('edit_course.html',
                                        currenttab=tab_set.get_tab(0),
                                        tabs=tab_set.get_tabs(),
                                        course=course)
            except KeyError:
                return '200 OK', render('error.html',
                                        currenttab=tab_set.get_tab(0),
                                        tabs=tab_set.get_tabs(),
                                        error='Ошибка редактирования курса')


# контроллер - копировать курс
@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            id = request_params['id']
            new_course = model_service.create_by_copy(type='course', id=id)
            new_course.observers.append(email_notifier)
            new_course.observers.append(sms_notifier)
            category_id = new_course.category
            category = model_service.find_by_id('category', int(category_id))
            category.courses.append(new_course)

            return '200 OK', render('course_list.html',
                                    currenttab=tab_set.get_tab(0),
                                    tabs=tab_set.get_tabs(),
                                    category=category,
                                    objects_list=category.courses)
        except KeyError:
            return '200 OK', render('error.html',
                                        currenttab=tab_set.get_tab(0),
                                        tabs=tab_set.get_tabs(),
                                        error='Copy failed')


@AppRoute(routes=routes, url='/timetable/')
class Timetable:
    def __call__(self, request):
        response = render('another-page.html',
                                date=request.get('date', None),
                                currenttab=tab_set.get_tab(1),
                                tabs=tab_set.get_tabs())
        return '200 OK', response


@AppRoute(routes=routes, url='/contactus/')
class ContactUs:

    def __call__(self, request):
        success = False
        if request['method'] == 'POST':
            message_data = request['data']
            del message_data['contact_submitted']
            new_message = DataForSave("MESSAGE", message_data)
            new_message.save(file_name='message.json')
            success = True,

        return '200 OK', render('contact.html',
                                    success=success,
                                    currenttab=tab_set.get_tab(3),
                                    tabs=tab_set.get_tabs())


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    tabs_desc = tabs
    tab_num = 2
    template_name = 'student_list.html'

    def get_context_data(self,):
        self.queryset = model_service.get_all("student")
        return super().get_context_data()


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(FormView):
    tabs_desc = tabs
    tab_num = 2
    template_name = 'create_student.html'

    def save_data(self, data: dict):
        name = model_service.decode_value(data['name'])
        email = model_service.decode_value(data['email'])
        attrs = {'name': name, 'email': email}
        model_service.create('student', attrs)


@AppRoute(routes=routes, url='/add-student-course/')
class AddStudentByCourseCreateView(FormView):
    tabs_desc = tabs
    tab_num = 2
    template_name = 'add-student-course.html'
    error = None

    def get_context_data(self, ):
        context = super().get_context_data()
        student_id = super().get_request_params()['id']
        try:
            context['courses'] = model_service.get_all("course")
        except Exception:
            pass
        context['student'] = model_service.find_by_id("student", student_id)
        return context

    def save_data(self, data: dict):
        try:
            course_id = data['course_id']
            course = model_service.find_by_id("course", course_id)

            student_id = super().get_request_params()['id']
            student = model_service.find_by_id("student", student_id)
            course.add_student(student)
        except KeyError:
            self.error = 'Ошибка сохранения'


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(model_service.get_all("course")).save()