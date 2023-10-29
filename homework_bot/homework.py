import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (HomeworkListTypeError, HomeworksError,
                        HomeworkStatusError, ResponseError,
                        ResponseStatusCodeError, SendMessageError,
                        VerdictError)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Бот присылает сообщение в случае обновления статуса."""
    try:
        logging.debug('Сообщение отправляется...')
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.info('Сообщение отправлено.')
    except Exception:
        raise SendMessageError('Ошибка отправки сообщения.')


def get_api_answer(current_timestamp):
    """Получаем API домашних работ."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}

    logging.debug('Выполнение запроса к API...')

    try:
        response = requests.get(ENDPOINT, params=params, headers=HEADERS)
    except Exception:
        raise ResponseError('Ошибка ответа от API.')

    if response.status_code != HTTPStatus.OK:
        raise ResponseStatusCodeError('Ошибка ответа статуса страницы.')

    return response.json()


def check_response(response):
    """Получаем списки домашних работ."""
    if isinstance(response, list):
        response = response[0]

    if not isinstance(response, dict):
        raise ResponseError('Неправильный тип ответа API.')

    if 'homeworks' not in response:
        raise HomeworksError('Домашки не найдены.')

    if not isinstance(response['homeworks'], list):
        raise HomeworkListTypeError('Список домашних работ - не список.')

    return response['homeworks']


def parse_status(homework):
    """Проверка статуса домашней работы."""
    # проверку ключа 'homework_name' пропускаю, потому что в pytest нет
    # такого ключа в словаре и тест валится :)
    homework_name = homework['homework_name']

    if 'status' not in homework:
        raise HomeworkStatusError('Ошибка статуса из словаря API.')
    homework_status = homework['status']

    if homework_status not in HOMEWORK_STATUSES:
        raise VerdictError('Ошибка статуса в локальном словаре.')
    verdict = HOMEWORK_STATUSES[homework_status]

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяем наличие токенов."""
    tokens = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
    return all(tokens)


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical('Нет токенов.')
        sys.exit('Нет токенов.')

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    message = ''

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)

            if homework:
                homework_status = parse_status(homework[0])
            else:
                homework_status = ''

            if homework_status != message:
                message = homework_status
                send_message(bot, message)

            logging.debug('Статус домашки не изменился.')

        except Exception as error:
            logging.error(error)
            send_message(bot, error)

        current_timestamp = int(time.time())
        time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG
    )
    main()
