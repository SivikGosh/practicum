from datetime import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    current = int(datetime.now().year)
    return {'year': current}
