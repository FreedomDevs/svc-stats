# svc-stats

Микросервис статистики игроков.

## Запуск

1. Запустить PostgreSQL
```bash
docker-compose up -d
```

2. Установить зависимости

```bash
pip install -r requirements.txt
```

3. Запустить сервис

```bash
python main.py
```

Сервис будет доступен на `http://127.0.0.1:9005`

---

## Эндпоинты

### Health

* `GET /live`

### Stats

* `POST /stats/{user_id}` — создать статистику
* `PUT /stats/{user_id}` — обновить статистику
* `GET /stats/{user_id}` — получить статистику
* `GET /stats?sort=kills&page=1&pageSize=20` — топ игроков с пагинацией

Поддерживаемая сортировка:

* `kills`
* `deaths`
* `time_played`

