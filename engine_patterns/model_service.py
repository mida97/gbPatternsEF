from quopri import decodestring
from engine_patterns.model_factory import ModelFactory
from engine_patterns.logger_singleton import Logger

logger = Logger('model_service')

# интерфейс получения данных и создания объектов
class ModelService:
    def __init__(self):
        self.objects = {
        'course': [],
        'category': [],
        'user': [],
        }

    def create(self, type, attrs):
        logger.log(f'Создание объекта {type}, c полями {attrs}')
        new_object = ModelFactory.create(type, attrs)

        self.objects[type].append(new_object)
        return new_object

    def edit(self, type, id, attrs):
        logger.log(f'Редактирование объекта {type} id = {id}, c полями {attrs}')
        object = self.find_by_id(type, id)
        object.edit(attrs)
        return object

    def create_by_copy(self, type, id):
        old_object = self.find_by_id(type='course', id=id)

        new_name = f'copy_of_{old_object.name}'
        new_object = old_object.clone()
        new_object.name = new_name

        logger.log(f'Копирование объекта {type}, c id {id}, новый id {new_object.id}')
        if type in self.objects:
            self.objects[type].append(new_object)
        else:
            self.objects[type] = [new_object, ]
        return new_object


    def find_by_id(self, type, id):
        if type not in self.objects:
            raise Exception(f'Объекта {type} не существет')
        for item in self.objects[type]:
            if item.id == int(id):
                return item
        raise Exception(f'Нет объекта {type} с id = {id}')


    def get_all(self, type):
        if type not in self.objects:
            raise Exception(f'Объекта {type} не существет')
        return self.objects[type]


    @staticmethod
    def decode_value(val):

        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')

