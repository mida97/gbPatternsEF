from copy import deepcopy
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


    def edit(self, attrs):
        for k, v in dict(attrs).items():
            setattr(self, k, v)
        logger.log(f'edit record {self.id}')

    def clone(self):
        new = super(Model, self).clone()
        new.id = self.get_seq()
        return new



#курс
class Course(Model):
    auto_id = -1

    @staticmethod
    def get_seq():
        Course.auto_id += 1
        return Course.auto_id

    def __init__(self, attrs):
        super().__init__(attrs)


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
        self.category = None

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class User:
    auto_id = -1

    @staticmethod
    def get_seq():
        User.auto_id += 1
        return User.auto_id

    def __init__(self, attrs):
        super().__init__(attrs)


class ModelFactory:

    types = {
        'course': Course,
        'category': Category,
        'user': User,
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, attrs):
        return cls.types[type_](attrs)

