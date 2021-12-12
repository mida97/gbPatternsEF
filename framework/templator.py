from pathlib import PurePath
from jinja2 import Template


def render(template_name, **kwargs):
    """
    Минимальный пример работы с шаблонизатором
    :param template_name: имя шаблона
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    path = PurePath(__file__).parent.parent / 'templates' / template_name

    with open(path, encoding='utf-8') as f:
        template = Template(f.read())

    return template.render(**kwargs).encode('utf-8')
