# svc-stats

Микросервис хранения и получения статистики игроков сети серверов Minecraft.


Поддерживаемые показатели:

- kills — количество убийств
    
- deaths — количество смертей
    
- time_played — время в игре
    

Все данные сохраняются в PostgreSQL и доступны через REST API.

---

# Запуск

Сервис запускается через **docker compose**.

```bash
docker compose up --build
```

После запуска будут подняты:

- **svc-stats-app** — приложение
    
- **svc-stats-postgres** — база данных
    

---

# Swagger

Документация:

```text
http://127.0.0.1:9005/docs
```

---

# Пример запросов

## Создание статистики игрока

POST

```http
/stats/{userId}?server_name=survival-1
```

Пример:

```http
POST /stats/c9a6467e-3d02-4f29-95c2-7a0c1d0c7c12?server_name=survival-1
```

Ответ:

HTTP `200 OK`

```json
{
  "data": {
    "user_id": "c9a6467e-3d02-4f29-95c2-7a0c1d0c7c12",
    "server_name": "survival-1"
  },
  "message": "Статистика создана",
  "meta": {
    "code": "STATS_CREATED"
  }
}
```

---

## Обновление статистики

PATCH

```http
/stats/{userId}?server_name=survival-1
```

Тело запроса:

```json
{
  "time_played": 3600,
  "kills": 15,
  "deaths": 4
}
```

Ответ:

```json
{
  "data": null,
  "message": "Статистика обновлена",
  "meta": {
    "code": "STATS_UPDATED"
  }
}
```

---

## Получение статистики игрока

GET

```http
/stats/{userId}?server_name=survival-1
```

Ответ:

```json
{
  "data": {
    "user_id": "c9a6467e-3d02-4f29-95c2-7a0c1d0c7c12",
    "server_name": "survival-1",
    "kills": 15,
    "deaths": 4,
    "time_played": 3600
  },
  "message": "Статистика получена",
  "meta": {
    "code": "STATS_FETCHED"
  }
}
```

---

## Получение таблицы лидеров

GET

```http
/stats?server_name=survival-1&sort=kills&page=1&pageSize=20
```

Доступные поля сортировки:

- kills
    
- deaths
    
- time_played
    

Ответ:

```json
{
  "data": {
    "items": [
      {
        "user_id": "c9a6467e-3d02-4f29-95c2-7a0c1d0c7c12",
        "kills": 15,
        "deaths": 4,
        "time_played": 3600
      }
    ]
  },
  "message": "Топ игроков получен",
  "meta": {
    "code": "STATS_LIST_FETCHED"
  },
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 100,
    "pages": 5
  }
}
```

---

## Проверка состояния сервиса

GET

```http
/live
```

Ответ:

```json
{
  "data": null,
  "message": "Service is alive",
  "meta": {
    "code": "LIVE_OK"
  }
}
```

---

# Эндпоинты

|Метод|Endpoint|Описание|
|---|---|---|
|GET|/live|Проверка состояния сервиса|
|POST|/stats/{userId}|Создать статистику игрока|
|PATCH|/stats/{userId}|Обновить статистику игрока|
|GET|/stats/{userId}|Получить статистику игрока|
|GET|/stats|Получить таблицу лидеров|

---

# Коды ответов

|Код|Описание|
|---|---|
|LIVE_OK|Сервис работает|
|STATS_CREATED|Статистика создана|
|STATS_UPDATED|Статистика обновлена|
|STATS_FETCHED|Статистика получена|
|STATS_LIST_FETCHED|Таблица лидеров получена|
|STATS_NOT_FOUND|Статистика не найдена|
|STATS_ALREADY_EXISTS|Статистика уже существует|
|VALIDATION_ERROR|Ошибка валидации данных|

---

# Модель статистики

```json
{
  "user_id": "UUID",
  "server_name": "survival-1",
  "kills": 0,
  "deaths": 0,
  "time_played": 0
}
```
