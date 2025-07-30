from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time
import os

def start_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 ...")
    options.add_argument("--log-level=3")

    service = Service(log_path="chrome_debug.log")  # niet naar console, maar wel naar bestand
    driver = webdriver.Chrome(options=options, service=service)
    return driver


def fetch_yahoo_financials(ticker):
    driver = start_driver()

    url = f"https://finance.yahoo.com/quote/{ticker}/financials"
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    # ✅ Stap 1: Cookie popup detecteren en accepteren
    try:
        accept_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Alles accepteren")]')
            )
        )
        accept_button.click()
        print("Cookies geaccepteerd.")
        time.sleep(1)  # wacht kort na klikken
    except:
        print("Geen cookie-popup gevonden of al geaccepteerd.")

    # ✅ Stap 2: Wacht tot de financiële tabel geladen is
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.tableContainer.yf-9ft13")))
    except:
        print("Waarschuwing: financiële tabel is niet gevonden.")

    # ✅ Stap 3: Pagina opslaan
    html = driver.page_source
    timestamp = time.strftime("%Y-%m-%d_%H-%M")
    os.makedirs(f"html/{ticker}", exist_ok=True)
    with open(f"html/{ticker}/{timestamp}.html", "w", encoding="utf-8") as f:
        f.write(html)

    # ✅ Stap 4: Data scrapen
    soup = BeautifulSoup(html, "html.parser")

    header_divs = soup.select("div.tableHeader div.column")
    headers = [h.text.strip() for h in header_divs]
    print(headers)

    rows = soup.find_all("div", class_="row lv-0 yf-t22klz")

    for row in rows:
        # Titel (linkerkant)
        title_div = row.find("div", class_="rowTitle")
        title = title_div.text.strip() if title_div else "?"

        # Data-cellen (zonder sticky kolom)
        data_divs = [
            div for div in row.find_all("div")
            if "column" in div.get("class", []) and
                "yf-t22klz" in div.get("class", []) and
                "sticky" not in div.get("class", [])
]
        values = [c.text.strip() for c in data_divs]

        print([title] + values)

    driver.quit()

# Test
fetch_yahoo_financials("BFIT.AS")
