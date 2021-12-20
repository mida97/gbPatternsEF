from pathlib import PurePath

# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name


    def log(self, text):
        print(f'log--->', text)

        path = PurePath(__file__).parent.parent / 'logs' / self.name

        with open(path, "a", encoding='UTF-8') as f:
            f.write(f'log---> {text}\n')