# CSV URL Decoder

Скрипт на Python для массового декодирования URL-адресов в CSV-файлах. Он извлекает ссылки (в том числе из Markdown-разметки) и преобразует percent-encoding (вида `%D0%A1...`) в читаемый текст (например, кириллицу), сохраняя все исходные данные файла.

## Особенности
- **Поддержка Markdown:** Умеет извлекать чистые ссылки из конструкций вида `[текст](https://...) -> https://...`.
- **Декодирование URL:** Корректно раскодирует UTF-8 URL (percent-encoding).
- **Неразрушающая обработка:** Сохраняет все оригинальные колонки из исходного CSV, добавляя новую колонку `decoded_url`.
- **Совместимость с Excel:** Сохраняет результат в кодировке `UTF-8 с BOM` (`utf-8-sig`), что исключает проблемы с отображением кракозябр (кириллицы) при открытии файла в Microsoft Excel.
- **Гибкость:** Управляется через удобный интерфейс командной строки (CLI).

## Требования
- Python 3.8 или выше.
- Библиотека `pandas`.

## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/3oltan-seo/csv-url-decoder.git
   cd csv-url-decoder
   ```
2. Установите необходимые библиотеки:
   ```bash
   pip install pandas
   ```

## Использование

Скрипт запускается из командной строки. Вы можете передать пути к файлам и название колонки в качестве аргументов.

```bash
python url-decoder.py -i <входной_файл.csv> -o <выходной_файл.csv> -c <название_колонки>
```

**Доступные параметры:**
* `-i`, `--input` : Путь к исходному CSV-файлу (по умолчанию: `GSC-more-1-click-1M-url.csv`).
* `-o`, `--output`: Путь для сохранения результата (по умолчанию: `GSC-more-1-click-1M-url_decoded.csv`).
* `-c`, `--column`: Имя колонки с URL-адресами, которую нужно декодировать (по умолчанию: `indexed_url`).

### Пример запуска

Если ваш файл называется `my_urls.csv` и колонка с ссылками называется `url`:

```bash
python url-decoder.py -i my_urls.csv -o result.csv -c url
```

Если вы просто запустите `python url-decoder.py` без аргументов, скрипт будет искать файл по умолчанию (`GSC-more-1-click-1M-url.csv`) и колонку `indexed_url`.

## Пример работы

**Входные данные (my_urls.csv):**
```csv
url,total_impressions,total_clicks
[https://ru.ruwiki.ru/wiki/%D0%9A%D0%BE%D0%BB%D0%BE%D0%B1%D1%83%D1%81%D1%8B](https://ru.ruwiki.ru/wiki/%D0%9A%D0%BE%D0%BB%D0%BE%D0%B1%D1%83%D1%81%D1%8B),20,0
```

**Выходные данные (result.csv):**
```csv
url,total_impressions,total_clicks,decoded_url
[https://ru.ruwiki.ru/wiki/%D0%9A%D0%BE%D0%BB%D0%BE%D0%B1%D1%83%D1%81%D1%8B](https://ru.ruwiki.ru/wiki/%D0%9A%D0%BE%D0%BB%D0%BE%D0%B1%D1%83%D1%81%D1%8B),20,0,https://ru.ruwiki.ru/wiki/Колобусы
```
