Проект доступен по адресу <http://158.160.54.114/>.
Данные для входа:
Логин: admin
Пароль: admin

# Foodrgam

 Продуктовый помощник - онлайн-сервис для составления рецептов и списков покупок.
 Проект реализован на `Django` и `DjangoRestFramework`.
 Доступ к данным реализован через API-интерфейс.
 Документация к API написана с использованием `Redoc`.

## Реализация

- Проект завернут в Docker-контейнеры;
- Образ бэкенд-части собран и запушен на DockerHub;
- Реализован workflow c автодеплоем на удаленный сервер;

## Развертывание проекта

### Развертывание на локальном сервере

1. Установите на сервере `docker` и `docker-compose`.
2. Создайте файл `/infra/.env`. Шаблон для заполнения файла нахоится в `/infra/.env example`.
3. Выполните команду `docker-compose up -d`.
4. Выполните миграции `docker-compose exec backend python manage.py migrate`.
5. Создайте суперпользователя `docker-compose exec backend python manage.py createsuperuser`.
6. Сбор статических файлов в единый каталог `docker-compose exec backend python manage.py collectstatic --no-input`.
7. Заполните базу ингредиентами `docker-compose exec backend python manage.py uploadcsv`.
8. **Для корректного создания рецепта через фронт, надо создать пару тегов в базе через админку.**
9. Документация к API находится по адресу: <http://localhost/api/docs/redoc.html>.

## Автор

 Георгий Маркаров (@SivikGosh)