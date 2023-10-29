"""Добавляет переменную с текущим годом"""

from datetime import datetime


def year(request):
    current = int(datetime.now().year)
    return {'year': current}
