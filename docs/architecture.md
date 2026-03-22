# Архитектура GeoAutoMap

## Назначение системы

GeoAutoMap предназначен для автоматического извлечения исторических событий из текстов и их последующей визуализации на карте, в таблице и на timeline.

Система строится как легкий production-like прототип с четким разделением на frontend, backend, слой сервисов и хранилище данных.

## Модульная схема

### Frontend

- React + TypeScript + Vite
- страницы: главная, документы, документ, карта, проверка, статистика
- интеграция с backend через REST API
- Leaflet-карта с кластеризацией маркеров

### Backend API

- FastAPI
- OpenAPI/Swagger
- маршруты для загрузки документов, запуска extraction pipeline, выборки событий, ручной правки и экспорта

### Слой данных

- PostgreSQL
- PostGIS
- Alembic migrations
- SQLAlchemy 2.x

### Сервисный слой

- `ingest_service` — загрузка и подготовка документов
- `parsers/*` — извлечение текста из `txt/docx/md/html/pdf`
- `llm/*` — prompts, Gemini client, validator, mock extractor
- `datetime_normalization/*` — нормализация временных выражений
- `geocoding/*` — локальный gazetteer, cache, Nominatim fallback
- `event_linking/*` — дедупликация и линковка событий
- `confidence/*` — финальная оценка уверенности
- `pipeline.py` — orchestration полного extraction flow

## Поток данных

```text
Файл/ручной текст
  -> ingest/parser
  -> clean text
  -> chunking
  -> LLM/Gemini или mock extractor
  -> JSON validation
  -> date normalization
  -> toponym normalization / geocoding
  -> confidence scoring
  -> сохранение events + PostGIS POINT
  -> экспорт CSV/JSON/GeoJSON
  -> frontend карта / таблица / review / stats
```

## Таблицы БД

### `documents`

Хранит документы и pipeline-статус.

### `text_chunks`

Хранит чанки документа, переданные в LLM.

### `events`

Основная таблица результатов extraction.  
Содержит нормализованные даты, топонимы, координаты и `geom`.

### `geocoding_cache`

Кэширует результаты геокодинга.

## Почему такая архитектура

- API и UI разделены и могут развиваться независимо
- LLM-слой инкапсулирован, поэтому можно заменить Gemini на другой провайдер
- mock режим позволяет работать без внешнего API
- geocoding и temporal normalization выделены в отдельные сервисы
- PostGIS закладывает основу для пространственной аналитики

## Расширение системы

В следующей итерации можно подключить:

- HeidelTime для более сильной temporal normalization
- Mordecai 3 для disambiguation топонимов
- MAVEN-совместимую схему richer event classes
- GeoNames как дополнительный источник координат
- отдельную очередь фоновых задач для extraction
