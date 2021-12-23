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

tabs_desc = [
    ['0', '/', 'Главная'],
    ['1', '/another_page/', 'Расписание'],
    ['2', '/contactus/', 'Обратная связь'],
]

tab_set = TabSet(tabs_desc)


#временно не используется
class Index_view:
    def __call__(self, request):
        response = render('index.html',
                      currenttab=tab_set.get_tab(0),
                      tabs=tab_set.get_tabs(),
                      objects_list=model_service.get_all('category'))
        return '200 OK', response


# контроллер - список категорий
@AppRoute(routes=routes, urls=['/category-list/', '/'])
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')

        return '200 OK', render('category_list.html',
                                currenttab=tab_set.get_tab(0),
                                tabs=tab_set.get_tabs(),
                                objects_list=model_service.get_all('category'))


# контроллер - список курсов
@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @Debug(name='CoursesList')
    def __call__(self, request):

        try:
            category = model_service.find_by_id('category', int(request['request_params']['id']))
            objects_list = category.courses
            logger.log('Список курсов для категории')
            return '200 OK', render('course_list.html',
                                    currenttab=tab_set.get_tab(0),
                                    tabs=tab_set.get_tabs(),
                                    category=category,
                                    objects_list=objects_list)
        except KeyError:
            objects_list = model_service.get_all('course')
            logger.log('Список всех курсов')
        return '200 OK', render('course_list.html',
                                currenttab=tab_set.get_tab(0),
                                tabs=tab_set.get_tabs(),
                                objects_list=objects_list)


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
class timetable:
    def __call__(self, request):
        response = render('another-page.html',
                                date=request.get('date', None),
                                currenttab=tab_set.get_tab(1),
                                tabs=tab_set.get_tabs())
        return '200 OK', response


@AppRoute(routes=routes, url='/contactus/')
class ContactUs:

    def __call__(self, request):

        if request['method'] == 'POST':
            message_data = request['data']
            del message_data['contact_submitted']
            new_message = DataForSave("MESSAGE", message_data)
            new_message.save(file_name='message.json')
            return '200 OK', render('contact.html',
                                        success=True,
                                        currenttab=tab_set.get_tab(2),
                                        tabs=tab_set.get_tabs())

        else:

            return '200 OK', render('contact.html',
                                        success=False,
                                        currenttab=tab_set.get_tab(2),
                                        tabs=tab_set.get_tabs())