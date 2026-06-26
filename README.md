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
   pip install -r requirements.txt
   ```
3. Создайте API-ключ в Outline: **Settings → API Keys**.
   - Scopes: `documents.info documents.documents` (или `documents.*`)
   - Можно оставить scopes пустым — ключ получит права вашего пользователя
4. Создайте файл конфигурации из примера:
   ```bash
   cp config.example.py config.py
   ```
5. Откройте `config.py` и заполните данные:
   - `API_KEY` — API-ключ Outline
   - `BASE_URL` — URL API (например, `https://docs.kts.tech/api`)
   - `TARGET_DOCUMENT_ID` — ID корневого документа, с которого начнётся экспорт (часть URL после `/doc/`, например `mangazeya-Dcq7UlrW1P`)
   - `OUTPUT_DIR` — папка для сохранения (по умолчанию `./outline_export`)

## Запуск

```bash
python3 export_outline.py
```

Скрипт получает дерево вложенных документов через `documents.documents`, скачивает текст каждого через `documents.info` и сохраняет `.md`-файлы с той же структурой папок, что и в Outline.

Результаты будут сохранены в папку, указанную в `OUTPUT_DIR`.
