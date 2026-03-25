# DocAI

Django REST Framework приложение для работы с документами и AI/RAG (Retrieval-Augmented Generation) сервисами.

## 📋 Описание

DocAI — это полнофункциональное приложение, которое объединяет возможности Django, Django REST Framework и современных AI технологий для работы с документами. Проект использует Weaviate как векторную базу данных для организации RAG сервисов.

### Основные возможности:

- 🔐 Аутентификация с использованием JWT токенов
- 📄 Управление документами и пользователями
- 🤖 RAG (Retrieval-Augmented Generation) функционал
- 🔍 Поиск с использованием векторной базы данных (Weaviate)
- 🌐 CORS поддержка для фронтенд интеграции
- 🐳 Docker Compose для простого развертывания
- ✅ Полное покрытие тестами

## 🛠️ Технологический стек

- **Backend**: Django 6.0+, Django REST Framework 3.16+
- **Python**: 3.12+
- **БД**: PostgreSQL
- **Vector DB**: Weaviate 1.30.0
- **Аутентификация**: SimpleJWT
- **CORS**: django-cors-headers
- **Образы обработки**: Pillow
- **Пакетный менеджер**: uv

## 📦 Установка

### Предварительные требования

- Python 3.12+
- uv (установить: `pip install uv`)
- Docker и Docker Compose (опционально, для локального развертывания)

### Локальная установка

1. **Клонируйте репозиторий**:
```bash
git clone <https://github.com/mukarramboy/DocAI.git>
cd DocAI
```

2. **Установите зависимости**:
```bash
uv sync
```

3. **Настройте переменные окружения**:
```bash
cp .env.example .env  # Если имеется
# Отредактируйте .env файл с необходимыми переменными
export SECRET_KEY="your-secret-key"
```

4. **Запустите миграции**:
```bash
make migrate
```

5. **Запустите сервер**:
```bash
make run
```

Сервер будет доступен по адресу `http://localhost:8000`

## 🐳 Запуск с Docker Compose

1. **Запустите контейнеры**:
```bash
docker-compose -f deploy/docker-compose.yml up -d
```

Это запустит:
- **Weaviate**: Векторная база данных (порт 8080, 50051)
- **Text2Vec Transformers**: Inference сервис для встраивания текста

2. **Выполните миграции** (если используется контейнер для Django):
```bash
docker-compose -f deploy/docker-compose.yml exec web make migrate
```

3. **Остановите контейнеры**:
```bash
docker-compose -f deploy/docker-compose.yml down
```

## 🚀 Использование

### Основные команды

| Команда | Описание |
|---------|----------|
| `make run` | Запуск сервера разработки |
| `make migrate` | Применить миграции БД |
| `make makemigrations` | Создать новые миграции |
| `make test` | Запустить тесты (pytest) |
| `make lint` | Проверить код (ruff) |
| `make format` | Отформатировать код |

### Пример API запроса

```bash
# Получить токен
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Использовать токен
curl -X GET http://localhost:8000/api/profile/ \
  -H "Authorization: Bearer <access_token>"
```

## 📁 Структура проекта

```
.
├── src/                          # Основной код приложения
│   ├── manage.py                # Django управление
│   ├── db.sqlite3               # SQLite БД (разработка)
│   ├── core/                    # Основные настройки Django
│   │   ├── settings/            # Конфигурация (base, developer, production)
│   │   ├── urls.py              # Главные маршруты
│   │   └── wsgi.py              # WSGI конфиг
│   ├── users/                   # App пользователей
│   │   ├── models.py            # Модели пользователей
│   │   ├── serializers.py       # DRF сериализаторы
│   │   ├── views.py             # API views
│   │   └── migrations/          # Миграции БД
│   ├── ai/                      # App AI функционала
│   │   ├── models.py            # Модели документов и т.д.
│   │   ├── views.py             # API views для AI
│   │   ├── services/            # Бизнес логика
│   │   │   ├── rag_service.py   # RAG сервис
│   │   │   └── chunking.py      # Разделение текста
│   │   ├── tools/               # Утилиты
│   │   │   └── search_tool.py   # Инструменты поиска
│   │   └── migrations/          # Миграции БД
│   └── media/                   # Загруженные файлы
├── tests/                       # Тесты проекта
│   └── conftest.py              # Конфиг pytest
├── deploy/
│   └── docker-compose.yml       # Docker контейнеры
├── pyproject.toml               # Конфиг проекта и зависимости
├── Makefile                     # Команды для разработки
└── README.md                    # Этот файл
```

## 🔧 Конфигурация

### Переменные окружения

Основные переменные окружения в `src/core/settings/base.py`:

```
SECRET_KEY=your-secret-key-here
DEBUG=False  # В production
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/docai
WEAVIATE_URL=http://localhost:8080
```

### Настройки по окружению

- **developer.py** - Настройки для разработки
- **production.py** - Настройки для продакшена
- **base.py** - Базовые настройки

Выбор окружения через переменную `DJANGO_SETTINGS_MODULE`:

```bash
export DJANGO_SETTINGS_MODULE=core.settings.production
```

## 🧪 Тестирование

Запуск тестов с помощью pytest:

```bash
# Все тесты
make test

# С покрытием
uv run pytest --cov

# Конкретный тест
uv run pytest tests/test_users.py
```

## 📚 API Документация

После запуска сервера документация доступна по адресам (если настроена):
- DRF UI: `http://localhost:8000/api/`
- ReDoc: `http://localhost:8000/redoc/` (если установлена)
- Swagger: `http://localhost:8000/swagger/` (если установлена)

## 🤝 Участие в разработке

1. Создайте ветку для вашей функции (`git checkout -b feature/AmazingFeature`)
2. Коммитьте изменения (`git commit -m 'Add some AmazingFeature'`)
3. Отправьте ветку (`git push origin feature/AmazingFeature`)
4. Откройте Pull Request

### Code Style

Проект использует **ruff** для линтинга и форматирования:

```bash
make lint    # Проверить стиль
make format  # Исправить стиль
```

## 📝 Лицензия

Укажите тип лицензии вашего проекта (например, MIT, Apache 2.0 и т.д.)

## 📞 Контакты

- **Разработчик**: [Ваше имя]
- **Email**: [Ваш email]
- **GitHub**: [Ваш GitHub профиль]

## 🔗 Полезные ссылки

- [Django документация](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Weaviate документация](https://weaviate.io/developers/weaviate)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)

---

**Последнее обновление**: Март 2026