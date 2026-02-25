# Outline Document Exporter

Скрипт для экспорта документов и их вложенной структуры из Outline в формат Markdown.

## Требования

- Python 3.x
- Библиотека `requests`

## Установка и настройка

1. Клонируйте репозиторий.
2. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install requests
   ```
3. Создайте файл конфигурации из примера:
   ```bash
   cp config.example.py config.py
   ```
4. Откройте `config.py` и заполните данные:
   - `API_KEY`: Ваш API ключ Outline.
   - `BASE_URL`: URL API (например, `https://docs.kts.tech/api`).
   - `COLLECTION_ID`: ID коллекции из URL.
   - `TARGET_DOCUMENT_ID`: ID корневого документа, с которого начнется экспорт.

## Запуск

```bash
python3 export_outline.py
```

Результаты будут сохранены в папку, указанную в `OUTPUT_DIR` (по умолчанию `./outline_export`).
