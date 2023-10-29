class SendMessageError(Exception):
    """Ошибка отправки сообщения."""
    pass


class ResponseError(Exception):
    """Ошибка ответа от API."""
    pass


class ResponseStatusCodeError(Exception):
    """Ошибка ответа статуса страницы."""
    pass


class HomeworksError(Exception):
    """Ошибка статуса домашней работы."""
    pass


class HomeworkListTypeError(Exception):
    """Ошибка типа списка домашек."""
    pass


class HomeworkStatusError(Exception):
    """Ошибка имени домашки."""
    pass


class VerdictError(Exception):
    """Ошибка статуса из локального словаря."""
    pass
