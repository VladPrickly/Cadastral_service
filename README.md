# Описание
API - сервис, который принимает запрос с указанием кадастрового номера, широты и долготы, эмулирует отправку запроса 
на внешний сервер, и может обрабатывать запрос до 60 секунд. Затем должен отдавать результат запроса. 
Внешний сервер может ответить true или false.

Данные запроса на сервер и ответ с внешнего сервера сохранены в БД. 

Сервис содержит следующие эндпоинты:
 - "POST /query" - принимает кадастровый номер
 - "GET /ping" - проверка, что сервер запустился
 - "GET /history" - для получения истории запросов
 - "GET /result" - эндпоинт эмулируемоего сервера, который возвращает true или false
 - "/docs" - документация Swagger для тестирования API
 - "/redoc" - документация ReDoc для тестирования API

## Предварительные требования
- Python 3.12+
- Git
- Docker и Docker Compose
- Доступ к интернету

## Структура проекта
  ```
  cadastral_service/
  ├── app/
  │   ├── __init__.py
  │   ├── config.py
  │   ├── db.py
  │   ├── lifespan.py
  │   ├── main.py
  │   ├── models.py
  │   └── schemas.py
  ├── alembic/
  │   ├── versions/
  │   ├── env.py
  │   └── script.py.mako
  ├── tests/
  │   ├── __init__.py
  │   ├── conftest.py
  │   └── test_api.py
  ├── README.md
  ├── .env
  ├── .env.example
  ├── alembic.ini
  ├── pytest.ini
  ├── init-test-db.sql
  ├── .gitignore
  ├── requirements.txt
  ├── Dockerfile
  └── docker-compose.yml
  ```

## Локальная установка 
1. Создайте виртуальное окружение:
- Windows:
  ```
  python -m venv .venv
  ```
- Linux/macOS:
  ```
  python3 -m venv .venv
  ```

2. Активируйте виртуальное окружение:
- Windows:
  ```
  .venv\Scripts\activate
  ```
- Linux/macOS:
  ```
  source .venv/bin/activate
  ```

3. Создайте переменные окружения (файл .env) по примеру .env.example
  ```
  POSTGRES_USER=user
  POSTGRES_PASSWORD=12345
  POSTGRES_DB=cadastral_db
  POSTGRES_HOST=db
  POSTGRES_PORT=5432
  ```

4. Установите зависимости
  ```
  pip install -r requirements.txt
  ```

5. Запустите приложение
  ```
  uvicorn app.main:app --reload --port 8000
  ```
## Запуск приложения и создание БД
  ```
  docker-compose build
  docker-compose up
  
  Приложение запустится локально на http://127.0.0.1:8000/. БД будет создана при первом запуске.
  ```

## Остановка приложения:
  ```
  docker-compose down
  ```

## Удаление контейнеров и томов:
  ```
  docker-compose down -v
  ```

## Создание миграций БД (Alembic)
  ```
  docker-compose run --rm app alembic revision --autogenerate -m "комментарий"
  ```

## Применение миграций БД
  ```
  docker-compose run --rm app alembic upgrade head
  ```

## Откатить последнюю миграцию
  ```
  docker-compose run --rm app alembic downgrade -1
  ```

## Проверка работы
  ```
  curl http://127.0.0.1:8000/ping
  Ожидаемый ответ: 
  {"status":"ok"}
  ```

  ```
  curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"cadastral_number": "77:01:1234567:890", "latitude": 56.78, "longitude": 43.21}'
  Ожидаемый ответ:
  {
    "id": 1,
    "cadastral_number": "77:01:1234567:890",
    "latitude": 56.78,
    "longitude": 43.21,
    "result": true,
    "created_at": "2026-07-27T21:34:56.789Z"
  }
  ```

  ```
  curl http://127.0.0.1:8000/result
  Ожидаемый ответ:
  {"result":true}
  ```

  ```
  curl http://127.0.0.1:8000/history
  Ожидаемый ответ:
  [
    {
      "id":2,
      "cadastral_number":"77:01:0987654:321",
      "latitude":22.33,
      "longitude":44.55,
      "result":true,
      "created_at":"2026-07-27T22:17:25.789353Z"
    },
    {
      "id":1,
      "cadastral_number":"77:01:1234567:890",
      "latitude":56.78,
      "longitude":43.21,
      "result":false,
      "created_at":"2026-07-27T21:58:50.819398Z"
    }
  ]
  ```

## Запуск тестирования внутри Docker-контейнера 
  ```
  docker-compose run --rm app pytest -v
  ```


## Автор
- Владислав
- telegram: @vlad_705
- [e-mail](vlad.prickly@gmail.com)
- [github.com](https://github.com/VladPrickly)

