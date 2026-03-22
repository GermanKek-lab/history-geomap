# GeoAutoMap

**GeoAutoMap — ИИ-система для построения карты исторических событий по текстам**  
Проект предназначен для извлечения событий из исторических источников, нормализации времени и топонимов, геокодинга и визуализации результатов на интерактивной карте.

## Авторы

1. Кек Герман, ИСУ 466149, поток истории ИРР 2.2
2. Зыков Макар, ИСУ 489608, поток истории ИРР 2.5
3. Урядов Валерий, ИСУ 467812, поток истории ИРС 1.4
4. Кулинич Павел, ИСУ 466420, поток истории ИРС 1.4

## Описание проекта

GeoAutoMap принимает текстовые исторические материалы в форматах `txt`, `docx`, `md`, `html`, `pdf`, выделяет из них исторические события и формирует структурированные записи со временем, местом, типом события, кратким описанием, уверенностью и цитатой из источника. Затем события сохраняются в PostgreSQL/PostGIS и показываются на карте, в таблице и на timeline.

Проект ориентирован на учебные кейсы:

- карты кампаний и сражений;
- реконструкцию маршрутов;
- анализ мемуарных свидетельств;
- построение хронологий и географии исторических процессов.

## Цель

Создать production-like прототип веб-продукта, который:

- принимает файлы и ручной ввод текста;
- извлекает исторические события через LLM pipeline;
- нормализует даты и топонимы;
- геокодирует места;
- сохраняет результат в БД;
- отображает события на карте и в интерфейсе с фильтрами;
- позволяет вручную исправлять извлеченные записи.

## Стек технологий

**Backend**

- Python 3.11
- FastAPI
- SQLAlchemy 2.x
- Pydantic v2
- PostgreSQL
- PostGIS
- Alembic
- Uvicorn

**NLP / LLM**

- Gemini API
- mock/fallback режим без API-ключа
- строгая JSON-валидация ответа
- модуль prompt templates

**Frontend**

- React
- TypeScript
- Vite
- Mantine
- Leaflet + clustering

**Инфраструктура**

- Docker
- docker-compose
- `.env.example`

## Архитектура

Ключевой поток данных:

`файл -> parser -> clean text -> chunking -> LLM/Gemini -> JSON validation -> date normalization -> geocoding -> confidence scoring -> PostgreSQL/PostGIS -> API -> React карта/таблица/review`

Основные слои:

- `backend/app/api` — REST API и OpenAPI
- `backend/app/db` — модели, сессии, репозитории
- `backend/app/services` — ingest, LLM, геокодинг, даты, confidence, pipeline
- `frontend/src` — страницы, компоненты, карта, фильтры, ручная проверка
- `sample_data` — демо-тексты и примеры выгрузок
- `scripts` — seed/export/demo pipeline
- `docs` — архитектура, API, сценарии демо, каркас отчета

## Структура проекта

```text
geoautomap/
  README.md
  .env.example
  docker-compose.yml
  docs/
  backend/
  frontend/
  sample_data/
  scripts/
```

Полная структура разложена по слоям в соответствии с заданием: backend, frontend, миграции, sample data, tests и документация уже включены в репозиторий.

## Быстрый запуск через Docker

1. Скопировать настройки:

```bash
cp .env.example .env
```

2. Поднять проект:

```bash
docker compose up --build
```

3. Открыть:

- frontend: `http://localhost:5173`
- backend API: `http://localhost:8000`
- Swagger/OpenAPI: `http://localhost:8000/docs`

В compose уже настроены:

- `healthcheck` для Postgres/PostGIS, backend и frontend;
- миграции Alembic перед стартом backend;
- CORS между frontend и backend.

## Локальный запуск без Docker

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Требования локальной среды

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+
- PostGIS extension

## Настройка `.env`

Основные переменные:

- `DATABASE_URL` — строка подключения SQLAlchemy
- `ALEMBIC_DATABASE_URL` — строка подключения для миграций
- `CORS_ORIGINS` — список origin через запятую
- `GEMINI_API_KEY` — ключ Gemini API
- `ENABLE_MOCK_LLM=true` — запуск в mock режиме без внешнего API
- `NOMINATIM_ENABLED=false` — включение внешнего геокодера
- `UPLOAD_DIR` — директория исходных файлов
- `EXPORT_DIR` — директория CSV/JSON/GeoJSON выгрузок

## Подключение Gemini API

1. Указать `GEMINI_API_KEY` в `.env`
2. При необходимости сменить `GEMINI_MODEL`
3. Запустить backend

Если ключ не задан или внешний вызов недоступен, pipeline автоматически переходит в mock режим. Это позволяет запускать проект офлайн и на демо-данных.

## Миграции

Применить миграции:

```bash
cd backend
alembic upgrade head
```

Создана начальная миграция `0001_initial.py`, которая:

- создает таблицы `documents`, `text_chunks`, `events`, `geocoding_cache`;
- создает индексы;
- включает PostGIS extension;
- создает `geom` типа `POINT`.

## Как открыть frontend

После старта откройте `http://localhost:5173`.

В интерфейсе доступны страницы:

- Главная
- Документы
- Карта
- Проверка
- Статистика

## Как загрузить тестовый документ

Вариант 1: через интерфейс на главной странице.

Вариант 2: использовать демо-файлы из `sample_data/texts`.

Вариант 3: загрузить текст вручную через textarea.

## Как запустить extraction pipeline

Через интерфейс:

1. Открыть страницу документа
2. Нажать `Извлечь события`
3. Дождаться обновления таблицы и timeline

Через API:

```bash
curl -X POST http://localhost:8000/api/documents/1/extract
```

## Как посмотреть события на карте

1. Открыть страницу `Карта`
2. Настроить фильтры по годам, типу события, документу, confidence и месту
3. Изучить маркеры, popup-карточки и таблицу справа

## CSV, JSON и GeoJSON экспорт

После extraction pipeline backend сохраняет:

- `document_<id>_events.csv`
- `document_<id>_events.json`
- `document_<id>_events.geojson`

Из интерфейса доступны кнопки экспорта CSV и JSON.  
Дополнительно есть скрипт `scripts/export_csv.py`, который умеет читать CSV и собирать GeoJSON.

### Использование в Google Maps

Практический путь для демонстрации:

1. Выполнить экспорт CSV
2. Проверить колонки `latitude`, `longitude`, `description`, `event_type`
3. Импортировать CSV вручную в Google My Maps
4. Либо сначала преобразовать CSV в GeoJSON и использовать этот файл как промежуточный слой

## Демо-данные

В репозитории уже есть:

- тексты про битву;
- текст про поход;
- текст-мемуар;
- текст-хроника;
- пример CSV;
- пример JSON;
- пример GeoJSON.

Полезные скрипты:

```bash
python scripts/seed_demo_data.py --extract
python scripts/run_demo_pipeline.py
python scripts/export_csv.py --from-csv sample_data/outputs/demo_events.csv --geojson-output sample_data/outputs/demo_events_from_csv.geojson
```

## API

Основные маршруты:

- `GET /health`
- `POST /api/upload`
- `GET /api/documents`
- `GET /api/documents/{id}`
- `GET /api/documents/{id}/text`
- `POST /api/documents/{id}/extract`
- `GET /api/events`
- `GET /api/events/{id}`
- `PATCH /api/events/{id}`
- `GET /api/events/map`
- `GET /api/events/stats`
- `GET /api/documents/{id}/export/csv`
- `GET /api/documents/{id}/export/json`
- `GET /api/geocoding/search?q=...`

Подробное описание и примеры — в `docs/api.md`.

## Соответствие учебному плану

Проект в коде и документации отражает этапы:

- **15–31 декабря 2025** — фиксируется JSON-схема события, собирается тестовый корпус
- **январь 2026** — MVP: топонимы, геокодинг, даты, таблица событий
- **февраль 2026** — извлечение действий/событий, связка место-время-событие, confidence
- **март 2026** — веб-интерфейс, карта, фильтры, PostGIS
- **апрель 2026** — кэш геокодинга, дизамбигуация топонимов, исторические варианты имен
- **май 2026** — полировка, документация, демо, ограничение модели и данных

## Архитектурные ориентиры и расширяемость

В проекте прямо учтены идеи и потенциальные точки расширения для:

- **Mordecai 3** — более сильная disambiguation логика по топонимам
- **HeidelTime** — специализированная нормализация времени
- **MAVEN** — richer event ontology и event typing
- **GeoNames** — альтернативный внешний геосервис
- **Nominatim** — легкий внешний геокодер
- **PostGIS** — пространственные запросы и геометрия событий

Сейчас интеграция сделана облегченной, чтобы MVP запускался локально и без внешних зависимостей.

## Ограничения проекта

- mock extractor использует эвристики и не заменяет полноценную историческую NER/event extraction модель;
- нормализация дат покрывает типовые, но не все исторические формулы;
- геокодинг исторических вариантов названий пока ограничен локальным справочником и fallback через Nominatim;
- confidence — эвристический агрегат, а не калиброванная метрика;
- автоматическое извлечение не гарантирует отсутствие ложноположительных или пропущенных событий.

## Возможные улучшения

- подключить реальный Gemini workflow с function calling;
- добавить версии событий и аудит правок проверяющего;
- вынести фоновые задачи extraction в Celery/RQ;
- расширить локальный gazetteer историческими названиями и GeoNames cache;
- подключить HeidelTime и специализированный temporal parser;
- добавить сравнение нескольких документов на одной карте;
- реализовать полноценный timeline chart и spatial analytics.

## Документация

- `docs/architecture.md`
- `docs/api.md`
- `docs/demo_scenarios.md`
- `docs/project_report_outline.md`
