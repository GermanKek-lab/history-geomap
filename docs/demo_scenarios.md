# Демо-сценарии

## Сценарий 1. Битва при Бородино

1. Загрузить `sample_data/texts/battle_borodino.txt`
2. Открыть карточку документа
3. Нажать `Извлечь события`
4. Показать событие типа `battle`
5. Перейти на страницу карты и отфильтровать `battle`

Что демонстрируется:

- ingest и parsing
- extraction pipeline
- геокодинг
- отображение на карте

## Сценарий 2. Поход и маневр

1. Загрузить `sample_data/texts/march_tarutino.md`
2. Выполнить extraction
3. Показать события типа `march`
4. Сравнить с битвой на общей карте

Что демонстрируется:

- парсинг markdown
- типизация событий
- фильтрация по типу и времени

## Сценарий 3. Мемуарный источник

1. Загрузить `sample_data/texts/memoir_sevastopol.html`
2. Выполнить extraction
3. Показать событие `memoir_reference`
4. Открыть ручную проверку и скорректировать confidence

Что демонстрируется:

- обработка html
- выделение мемуарного фрагмента
- human-in-the-loop

## Сценарий 4. Историческая хроника

1. Загрузить `sample_data/texts/chronicle_pskov.txt`
2. Выполнить extraction
3. Показать нормализацию даты `в начале XIX века`
4. Показать сохранение period label и диапазона дат

Что демонстрируется:

- нечеткие даты
- нормализация эпох и периодов
- timeline и статистика

## Сценарий 5. Экспорт в CSV / GeoJSON

1. После extraction скачать CSV с карточки документа
2. Запустить:

```bash
python scripts/export_csv.py --from-csv sample_data/outputs/demo_events.csv --geojson-output sample_data/outputs/demo_events_from_csv.geojson
```

3. Импортировать CSV в Google My Maps
4. Показать альтернативную загрузку GeoJSON

Что демонстрируется:

- промежуточный CSV
- GeoJSON-конвертация
- интеграционный сценарий для картографических сервисов
