import re
import argparse
import pandas as pd
from urllib.parse import unquote

# Регулярка для markdown-ссылок вида [текст](URL)
MD_LINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+)\)')


def extract_url(raw: str) -> str:
    """
    Извлекает реальный URL из строки:
    - "[text](https://site/path%20x)" -> "https://site/path%20x"
    - "https://site/path%20x"         -> "https://site/path%20x"
    """
    if pd.isna(raw) or raw is None:
        return ""
    s = str(raw).strip()
    m = MD_LINK_RE.match(s)
    if m:
        return m.group(1)
    return s


def decode_urls_in_csv(input_csv: str, output_csv: str, url_column: str = "url") -> None:
    """
    Читает CSV-файл, находит колонку с URL, извлекает чистые ссылки,
    декодирует их (url-decode) и сохраняет все данные в новый CSV-файл.
    """
    try:
        # Читаем CSV (все колонки)
        df = pd.read_csv(input_csv, encoding="utf-8")
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_csv}' не найден. Убедитесь, что путь указан верно.")
        return

    if url_column not in df.columns:
        print(f"Ошибка: Колонка '{url_column}' не найдена в файле '{input_csv}'.")
        print(f"Доступные колонки: {', '.join(df.columns)}")
        return

    def transform(value):
        if pd.isna(value):
            return value
        raw_url = extract_url(value)
        return unquote(raw_url)

    # Добавляем НОВУЮ колонку, не изменяя старые
    df["decoded_url"] = df[url_column].apply(transform)

    # Сохраняем все колонки в новый CSV (utf-8-sig — удобно для открытия в Excel)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"Успех! Файл сохранен как '{output_csv}'. Обработано строк: {len(df)}")


if __name__ == "__main__":
    # Настройка аргументов командной строки для гибкости
    parser = argparse.ArgumentParser(description="Декодирование URL-адресов в CSV-файле.")
    parser.add_argument("-i", "--input", default="GSC-more-1-click-1M-url.csv", help="Путь к исходному CSV-файлу")
    parser.add_argument("-o", "--output", default="GSC-more-1-click-1M-url_decoded.csv", help="Путь для сохранения результата")
    parser.add_argument("-c", "--column", default="indexed_url", help="Имя колонки с URL-адресами")

    args = parser.parse_args()

    decode_urls_in_csv(
        input_csv=args.input,
        output_csv=args.output,
        url_column=args.column,
    )