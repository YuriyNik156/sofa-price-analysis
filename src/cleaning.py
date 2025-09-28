import os
import pandas as pd


# определяем путь до конца проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw_products.csv")
CLEAN_PATH = os.path.join(BASE_DIR, "data", "cleaned_products.csv")


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


def main():
    if not os.path.exists(RAW_PATH):
        print(f"⚠ Файл {RAW_PATH} не найден")
        return

    df = pd.read_csv(RAW_PATH)

    # очистка цен
    df["price"] = df["price"].apply(clean_price)

    # удаление строки без цены
    df = df.dropna(subset=["price"])

    # сохранение
    df.to_csv(CLEAN_PATH, index=False, encoding="utf-8")
    print(f"✅ Очищенные данные сохранены в {CLEAN_PATH}")


if __name__ == "__main__":
    main()