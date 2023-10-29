# ![](https://praktikum.s3.yandex.net/praktikum/v1.61-1665995254/static/favicon-32x32.png) Проект «API для Yatube»
*Модуль для интеграции API в проект Yatube.*

*Умеет формировать JSON-словари с объектам пользователей и их подписчиков, публикаций и комментариев к ним.*

*К модулю приложена подробная документация с описанием всех реализованных эндпоинтов. Что значительно облегчило написанию мной данного проекта. :)*

*Пару примеров полученных данных будет представлено ниже.*

-----

## Установка
*Клонируйте репозиторий:*
> git clone ```git@github.com:SivikGosh/api_final_yatube.git```

*Установите виртуальное и запустите виртуальное окружение:*
* > py -3.7 venv venv
* > source venv/Scripts/activate (Windows)
* > source venv/bin/activate (Linux)

*Установите зависимости:*
* > pip install -r requirements.txt (Windows)
* > pip3.7 install -r requirements.txt (Linux)

-----

## Запуск
*Запустите миграции моделей:*
* > cd yatube_api/
* > python manage.py migrate
*Запустите проект на локальном сервере:*
* > python manage.py runserver

*Корневой адрес проекта* http://localhost:8000/ .

-----

## Пара примеров
*Получаем список публикаций по **GET**-запросу к эндпоинту **posts/** :*
```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```

*Получаем конкретный пост по его **ID**, например **posts/1/** :*
```
{
  "id": 1,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 1
}
```

*Полный список эндпоинтов находится в документации по адресу проекта http://localhost:8000/redoc/ .*

-----

Автор проекта [@SivikGosh](https://t.me/SivikGosh) .
