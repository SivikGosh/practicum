""" добавление текущего года в контекст шаблона """

from datetime import datetime


def year(request):
    return {'year': int(datetime.now().year)}
