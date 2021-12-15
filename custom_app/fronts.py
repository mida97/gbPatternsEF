from datetime import datetime


def auth_front(request):
    # здесь может быть логика аутентификации
    request['username'] = 'user'
    request['userrole'] = 'role'


def time_front(request):
    request['date'] = str(datetime.today()).split()[0]


fronts = [auth_front, time_front]