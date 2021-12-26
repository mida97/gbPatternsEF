from copy import deepcopy

from engine_patterns.behavioral_patterns import Subject
from engine_patterns.logger_singleton import Logger


logger = Logger('model')


# порождающий паттерн Прототип интерфейс для копирования объектов
class Prototype:

    def clone(self):
        return deepcopy(self)


# Супер-класс для всех моделей
class Model(Prototype):
    @staticmethod
    def get_seq():
        pass

    def __init__(self, attrs):
        self.id = self.get_seq()
        for k, v in dict(attrs).items():
            setattr(self, k, v)
        logger.log(f'create new record {self.id}')

    def get_attr(self, attrname):
        return object.__getattribute__(self, attrname)

    def edit(self, attrs):
        for k, v in dict(attrs).items():
            setattr(self, k, v)
        logger.log(f'edit record {self.id}')

    def clone(self):
        new = super(Model, self).clone()
        new.id = self.get_seq()
        return new


#курс Subject реализует паттерн наблюдатель
class Course(Model, Subject):
    auto_id = -1

    @staticmethod
    def get_seq():
        Course.auto_id += 1
        return Course.auto_id

    def __init__(self, attrs):
        super().__init__(attrs)
        self.observers = []
        self.students = []

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student):
        self.students.append(student)
        student.courses.append(self)
        self.notify(f'Новый студент {student.name} на курсе {self.name}')

    def edit(self, attrs):
        super().edit(attrs)
        self.notify(f'Курс {self.name} изменен')


# категория
class Category(Model):
    auto_id = -1

    @staticmethod
    def get_seq():
        Category.auto_id += 1
        return Category.auto_id

    def __init__(self, attrs):
        super().__init__(attrs)
        self.courses = []
        self.children = []

    def course_count(self):
        result = len(self.courses)
        if self.children:
            for c in self.children:
                result += c.course_count()
        return result

    def update_fullname(self):
        result = str(self.name)
        if self.parent:
            result = self.parent.fullname + '/' + result
        self.fullname = result


class User(Model):
    auto_id = -1

    @staticmethod
    def get_seq():
        User.auto_id += 1
        return User.auto_id

    def __init__(self, attrs):
        super().__init__(attrs)


class Student(User):
    def __init__(self, attrs):
        super().__init__(attrs)
        self.courses = []
        self.role = 'student'


class ModelFactory:

    types = {
        'course': Course,
        'category': Category,
        'student': Student,
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, attrs):
        return cls.types[type_](attrs)

