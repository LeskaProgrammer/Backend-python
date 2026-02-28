# Notes API

ДЗ6 по бэкенду на питоне

## Что добавлено в ДЗ6

- Миграция данных (`0002_seed_data.py`) — моковые данные (4 пользователя, 7 заметок, 8 комментариев, лайки)
- Сериализаторы для NoteLike, CommentLike + легковесные (NoteLightSerializer, CommentLightSerializer)
- ViewSets для всех моделей, включая ReadOnly для лайков
- Кастомные агрегированные эндпоинты: `popular`, `pinned`, `stats`, `lightweight`, `top_by_notes`, `top_by_comments`, `by_author`
- Dockerfile для поднятия бэкенда
- Инструкция по применению миграций в README

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

## Применение миграций

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
```

После `migrate` автоматически создаются тестовые данные (миграция `0002_seed_data`):
- admin / admin123 (суперпользователь)
- ivan_ivanov / password123
- maria_petrova / password123
- alex_smirnov / password123
