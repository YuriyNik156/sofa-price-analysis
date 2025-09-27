import requests
from bs4 import BeautifulSoup
import csv
import time
import random


BASE_URL = "https://www.divan.ru/category/divany-i-kresla"
OUTPUT_FILE = "../data/raw_products.csv"


def fetch_page(url: str) -> str | None:
    """Загрузка HTML-страницы и возврат текста или None при ошибке"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[Ошибка] Не удалось загрузить страницу {url}: {e}")
        return None


def parse_products(html: str) -> list[dict]:
    """Парсинг товаров с одной категории divany-i-kresla"""
    soup = BeautifulSoup(html, "html.parser")
    products = []

    items = soup.find_all("div", class_="lsooF")
    for item in items:
        try:
            name = item.find("span", class_="pY3d2").get_text(strip=True)
        except AttributeError:
            name = None

        try:
            price = item.find("span", class_="ui-LD-ZU KIkOH").get_text(strip=True)
        except AttributeError:
            price = None

        try:
            link = item.find("a", class_="ui-GPFV8 qUioe")["href"]
            link = "https://www.divan.ru/category/divany-i-kresla" + link
        except (AttributeError, TypeError):
            link = None

        if name and price and link:
            products.append({
                "name": name,
                "price": price,
                "link": link
            })
        else:
            print("[Предупреждение] Пропущен товар из-за неполных данных.")

    return products







# Запускаем браузер
driver = webdriver.Chrome()

# Открываем страницу с диванами
url = "https://www.divan.ru/category/divany-i-kresla"
driver.get(url)
time.sleep(5)

price_text = driver.find_elements(By.CLASS_NAME, "ui-LD-ZU")

# Создание и открытие CSV-файла для записи
with open("products.csv", mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Цены на диваны"])  # Указываем заголовок столбца

    # Запись данных в файл
    for price in price_text:
        writer.writerow([price.text])

print("Данные успешно сохранены в файл products.csv")

# Закрытие браузера
driver.quit()