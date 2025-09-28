import os
import pandas as pd
import numpy as np
from scipy import stats


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLEAN_PATH = os.path.join(BASE_DIR, "data", "cleaned_products.csv")


def main():
    if not os.path.exists(CLEAN_PATH):
        print(f"⚠ Файл {CLEAN_PATH} не найден. Сначала запусти cleaning.py")
        return

    df = pd.read_csv(CLEAN_PATH)

    print("\n📊 Информация о данных:")
    print(df.info())

    print("\n📈 Статистика:")
    print(df.describe())

    prices = df["price"].dropna()

    # метрики
    mean_price = prices.mean()
    median_price = prices.median()
    try:
        mode_price = stats.mode(prices, keepdims=True).mode[0]
    except Exception:
        mode_price = None

    q1 = prices.quantile(0.25)
    q3 = prices.quantile(0.75)
    iqr = q3 - q1
    std = prices.std()
    outliers = (prices > q3 + 1.5 * iqr).sum()

    print("\n📌 Метрики:")
    print(f"Средняя цена: {mean_price:,.0f} ₽")
    print(f"Медиана: {median_price:,.0f} ₽")
    print(f"Мода: {mode_price:,.0f} ₽" if mode_price else "Мода: не найдена")
    print(f"Q1: {q1:,.0f} ₽, Q3: {q3:,.0f} ₽")
    print(f"IQR: {iqr:,.0f} ₽")
    print(f"Стандартное отклонение: {std:,.0f} ₽")
    print(f"Количество выбросов (> Q3 + 1.5*IQR): {outliers}")


if __name__ == "__main__":
    main()