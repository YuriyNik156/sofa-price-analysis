import os
import pandas as pd


RAW_PATH = os.path.join("data", "raw_products.csv")
CLEAN_PATH = os.path.join("data", "cleaned_products.csv")


def clean_price(price_str):
    """
    Очистка цен:
    - удаление ₽ и пробелов
    - сохранение только чисел
    - конвертация во float или None
    """
    if not isinstance(price_str, str):
        return None
    cleaned = (
        price_str.replace("₽", "")
        .replace("\xa0", "")
        .replace(" ", "")
        .strip()
    )
    if cleaned.isdigit():
        return int(cleaned)
    return None


