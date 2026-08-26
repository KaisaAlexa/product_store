# Django MySite

Веб-приложение на Django, объединяющее интернет-магазин, блог и модуль аутентификации пользователей.

## Возможности

### Shop (`/shop/`)
- Каталог товаров с ценой, скидкой, описанием и изображениями
- Создание, редактирование и архивация товаров
- Управление заказами и экспорт данных в CSV
- REST API для товаров (`/shop/api/products/`)
- RSS-лента последних товаров

### Blog (`/blog/`)
- Публикация статей с авторами, категориями и тегами
- Список статей с фильтрацией

### Auth (`/myauth/`)
- Регистрация и вход пользователей
- Страница профиля
- Работа с cookies и sessions

### Прочее
- Админ-панель Django (`/admin/`)
- Карта сайта (`/sitemap.xml`)
- Кэширование и sitemap для SEO

## Стек технологий

- Python 3.11
- Django 4.2
- Django REST Framework
- django-filter
- Pillow
- Gunicorn + WhiteNoise
- Poetry
- Docker / Docker Compose
- SQLite

## Структура проекта

```
django-mysite/
├── mysite/              # Django-проект
│   ├── shopapp/         # магазин
│   ├── blogapp/         # блог
│   ├── myauth/          # аутентификация
│   └── mysite/          # настройки
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── pyproject.toml
└── poetry.lock
```

## Быстрый старт (Docker)

```bash
cp .env.example .env
docker compose up --build -d
docker compose exec web python manage.py createsuperuser
```

Приложение будет доступно по адресу: http://localhost:8000

Основные страницы:
- http://localhost:8000/shop/
- http://localhost:8000/blog/
- http://localhost:8000/myauth/login/
- http://localhost:8000/admin/

## Локальная разработка (Poetry)

```bash
poetry install
cd mysite
poetry run python manage.py migrate
poetry run python manage.py runserver
```

## Переменные окружения

| Переменная | Описание |
|---|---|
| `DJANGO_SECRET_KEY` | Секретный ключ Django |
| `DJANGO_ALLOWED_HOSTS` | Разрешённые хосты через запятую |
| `DJANGO_DB_NAME` | Путь к файлу SQLite (по умолчанию `data/db.sqlite3`) |

## Деплой

Приложение готово к публикации на сервере через Docker Compose с политикой `restart: always`. При старте контейнера автоматически выполняются миграции и сбор статики (`collectstatic`).
