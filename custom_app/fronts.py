import time


def auth_front(request):
    # здесь может быть логика аутентификации
    request['username'] = 'user'
    request['userrole'] = 'role'


def time_front(request):
    request['request_time'] = time.time()


fronts = [auth_front, time_front]