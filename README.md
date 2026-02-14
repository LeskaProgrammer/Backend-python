# Notes API

ДЗ5 по бэкенду на Python (Django + Django REST Framework)

## Что сделано

- Создан Django проект с приложением notes
- Описаны 4 модели: Note, Comment, NoteLike, CommentLike
- Реализованы ViewSets с кастомными actions (like/unlike/pin/unpin)
- Подключен Swagger (drf-spectacular)
- Все модели зарегистрированы в админке с фильтрами и поиском
- Написан Makefile для удобного запуска
- Подготовлен Docker для PostgreSQL

## Возможности

- CRUD для пользователей, заметок и комментариев
- Лайки для заметок и комментариев
- Закрепление заметок
- Поиск по заметкам
- Фильтрация комментариев по заметке
- Swagger документация (`/api/docs/`)
- Админ-панель (`/admin/`)

## Структура проекта

```
notes_api/
├── storage/                  # Docker окружение для БД
│   ├── Dockerfile            # образ PostgreSQL
│   ├── docker-compose.yml    # конфигурация контейнера
│   └── init.sh               # скрипт инициализации БД
└── backend/                  # Django проект
    ├── config/               # настройки проекта
    │   ├── settings.py       # конфигурация Django
    │   └── urls.py           # главные маршруты
    ├── notes/                # приложение заметок
    │   ├── models.py         # модели данных
    │   ├── views.py          # ViewSets (API логика)
    │   ├── serializers.py    # сериализаторы DRF
    │   ├── urls.py           # маршруты API
    │   └── admin.py          # регистрация в админке
    ├── requirements.txt      # зависимости Python
    └── Makefile              # команды для запуска
```
