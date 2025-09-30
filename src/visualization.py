import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.cleaning import CLEAN_PATH

# Пути
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_PATH = os.path.join(BASE_DIR, "data", "cleaned_products.csv")
IMG_DIR = os.path.join(BASE_DIR, "reports", "figures")

os.makedirs(IMG_DIR, exist_ok=True)


def main():
    # Загрузка данных
    df = pd.read_csv(CLEAN_PATH)

    # --- Гистограмма цен ---
    plt.figure(figsize=(8, 5))
    sns.histplot(df["price"], bins=30, kde=False)
    plt.title("Гистограммы цен на товары мебели")
    plt.xlabel("Цена, ₽")
    plt.ylabel("Количество диванов")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, "histogram_prices.png"))
    plt.close()

    # --- Boxplot ---
    plt.figure(figsize=(6, 4))
    sns.boxplot(x=df["price"])
    plt.title("Boxplot цен на диваны (выбросы)")
    plt.xlabel("Цена, ₽")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, "boxplot_prices.png"))
    plt.close()

    # --- KDE-график ---
    plt.figure(figsize=(8, 5))
    sns.kdeplot(df["price"], fill=True)
    plt.title("KDE-график распределения цен")
    plt.xlabel("Цена, ₽")
    plt.ylabel("Плотность")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, "scatter_name_length_vs_price.png"))
    plt.close()

    print(f"✅ Все графики сохранены в {IMG_DIR}")


if __name__ == "__main__":
    main()
    