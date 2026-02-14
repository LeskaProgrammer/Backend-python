# Notes API

ДЗ5 по бэкенду на Python (Django REST Framework)

## Возможности

- CRUD для пользователей, заметок и комментариев
- Лайки для заметок и комментариев
- Закрепление заметок
- Поиск по заметкам
- Фильтрация комментариев по заметке
- Swagger документация
- Админ-панель

## Структура проекта

```
notes_api/
├── storage/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── init.sh
└── backend/
    ├── config/
    │   ├── settings.py
    │   └── urls.py
    ├── notes/
    │   ├── models.py
    │   ├── views.py
    │   ├── serializers.py
    │   ├── urls.py
    │   └── admin.py
    ├── requirements.txt
    └── Makefile
```
