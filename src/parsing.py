from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv

OUTPUT_FILE = "../data/raw_products.csv"
BASE_URL = "https://www.divan.ru/category/divany-i-kresla"


def parse_products(driver):
    products = []
    items = driver.find_elements(By.CSS_SELECTOR, "a.ProductName")
    for item in items:
        try:
            name = item.find_element(By.CSS_SELECTOR, "span[itemprop='name']").text.strip()
            price = item.find_element(By.XPATH, "../../..//span[@data-testid='price']").text.strip()
            link = item.get_attribute("href")
            products.append({"name": name, "price": price, "link": link})
        except Exception:
            print("[Предупреждение] Пропущен товар (неполные данные)")
    return products


def main():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")  # если хочешь видеть браузер, закомментируй

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    all_products = []

    try:
        for page in range(1, 6):
            url = f"{BASE_URL}?page={page}"
            print(f"[INFO] Загружаю {url}")
            driver.get(url)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.ProductName")
                )
            except Exception:
                print("[Ошибка] Карточки диванов не найдены на странице")
                continue

            products = parse_products(driver)
            all_products.extend(products)

            if len(all_products) >= 100:
                break

    finally:
        driver.quit()  # теперь сессия всегда корректно закрывается

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "link"])
        writer.writeheader()
        writer.writerows(all_products[:100])

    print(f"[OK] Сохранено {len(all_products[:100])} товаров в {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
