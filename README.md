[![Foodgram deployy latestss](https://github.com/platonov1727/foodgram-project-react/actions/workflows/django.yml/badge.svg)](https://github.com/platonov1727/foodgram-project-react/actions/workflows/django.yml)

# 62.84.123.55
'''
login: platonov1727@yandex.ry
password: 123
'''

# Фудграмм - дипломный проект

## Описание

Сервис в котором пользователи могут делиться рецептами и выкладывать свои, подписываться на авторов и скачивать ингредиенты понравившихся рецептов для дальнейшей покупки.

## Подробная документация по адресу YOURHOST/redoc/

В redoc описанны все ендпоинты и их возможности с примерами запросов. И ожидаемые ответы.

## Возможности

- Аутентификация по токену
- возможность ознакомиться с рецептами без аутентификации

## Технологии

- Django==3.2
- django-filter==22.1
- django-import-export==3.0.2
- djangorestframework==3.12.4
- djangorestframework-simplejwt==5.2.2
- PyJWT==2.1.0

со списком всех используемых библиотек можно ознакомиться в файлe requirements.txt

## Инструкции по развертыванию проекта в dev режиме

## Запуск проекта в dev-режиме

```code
git clone <название репозитория>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
Load test data in django admin panel
python manage.py runserver
```

## Инструкции по развертыванию проекта в docker

- Установите Docker, используя инструкции с официального сайта.
- Склонируйте репозиторий на локальную машину

```code
git clone git@github.com:platonov1727/yamdb_final.git
```

- Создайте файл .env командой

```code
touch .env
```

- Добавьте в него переменные окружения для работы с базой данных:
- Запустите docker-compose командой

```code
sudo docker-compose up -d
```

- Выполните миграции

```code
sudo docker-compose exec yamdb python manage.py migrate
```

- Соберите статику командой

```code
sudo docker-compose exec yamdb python manage.py collectstatic --no-input
```

- Создайте суперпользователя Django

```code
sudo docker-compose exec yamdb python manage.py createsuperuser --username admin --email 'admin@yamdb.com'
```
