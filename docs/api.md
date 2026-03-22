# API GeoAutoMap

## Базовый URL

`http://localhost:8000`

Swagger/OpenAPI: `http://localhost:8000/docs`

## 1. Health

### `GET /health`

Проверка состояния backend и подключения к БД.

Пример ответа:

```json
{
  "status": "ok",
  "service": "GeoAutoMap",
  "environment": "development",
  "database": true
}
```

## 2. Upload

### `POST /api/upload`

Поддерживает:

- `file` — multipart upload
- `manual_text` — ручной текст
- `manual_filename` — имя для ручного текста

Пример ответа:

```json
{
  "id": 1,
  "filename": "battle_borodino.txt",
  "format": "txt",
  "source_type": "file",
  "processing_status": "uploaded",
  "last_error": null,
  "uploaded_at": "2026-03-22T00:00:00Z",
  "chunks_count": 0,
  "events_count": 0,
  "storage_path": "data/uploads/battle_borodino.txt",
  "original_text": "7 сентября 1812 года..."
}
```

## 3. Documents

### `GET /api/documents`

Возвращает список документов.

### `GET /api/documents/{id}`

Карточка документа.

### `GET /api/documents/{id}/text`

Исходный текст документа.

### `POST /api/documents/{id}/extract`

Запускает полный pipeline extraction.

Пример ответа:

```json
{
  "document_id": 1,
  "status": "completed",
  "chunks_created": 2,
  "events_created": 3,
  "warnings": [],
  "csv_path": "sample_data/outputs/document_1_events.csv",
  "json_path": "sample_data/outputs/document_1_events.json",
  "geojson_path": "sample_data/outputs/document_1_events.geojson"
}
```

### `GET /api/documents/{id}/export/csv`

Отдает CSV-файл с событиями.

### `GET /api/documents/{id}/export/json`

Отдает JSON-экспорт.

## 4. Events

### `GET /api/events`

Фильтры:

- `document_id`
- `year_from`
- `year_to`
- `event_type`
- `min_confidence`
- `place_query`

Пример:

```bash
curl "http://localhost:8000/api/events?event_type=battle&year_from=1812&min_confidence=0.7"
```

### `GET /api/events/{id}`

Карточка события.

### `PATCH /api/events/{id}`

Ручное редактирование.

Пример запроса:

```json
{
  "place_name_raw": "Бородино",
  "place_name_normalized": "Бородино",
  "latitude": 55.529,
  "longitude": 35.818,
  "confidence": 0.94,
  "reviewer_comment": "Координаты подтверждены вручную",
  "is_reviewed": true
}
```

## 5. Карта

### `GET /api/events/map`

Возвращает GeoJSON `FeatureCollection`.

Пример ответа:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [35.818, 55.529]
      },
      "properties": {
        "id": 1,
        "event_type": "battle",
        "description": "Крупное сражение между русской армией и армией Наполеона"
      }
    }
  ]
}
```

## 6. Statistics

### `GET /api/events/stats`

Возвращает:

- общее число событий
- число проверенных вручную
- число записей без координат
- распределения по типам, периодам и годам

## 7. Geocoding

### `GET /api/geocoding/search?q=Бородино`

Проверка результата геокодинга для конкретного топонима.

Пример ответа:

```json
{
  "query": "Бородино",
  "normalized_name": "Бородино",
  "latitude": 55.529,
  "longitude": 35.818,
  "source": "local_gazetteer",
  "confidence": 0.95
}
```
