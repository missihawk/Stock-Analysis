# fetch/financials.py
from bs4 import BeautifulSoup
import pandas as pd
import time, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_financials(driver, ticker: str, save_html: bool = False) -> pd.DataFrame:
    url = f"https://finance.yahoo.com/quote/{ticker}/financials"
    driver.get(url)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    wait = WebDriverWait(driver, 10)

    # Wacht op table container
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.tableContainer.yf-9ft13")))
    except:
        print(f"[{ticker}] ⚠️ Tabel niet gevonden.")

    # HTML opslaan (optioneel)
    html = driver.page_source
    if save_html:
        timestamp = time.strftime("%Y-%m-%d_%H-%M")
        os.makedirs(f"html/{ticker}", exist_ok=True)
        with open(f"html/{ticker}/{timestamp}.html", "w", encoding="utf-8") as f:
            f.write(html)

    soup = BeautifulSoup(html, "html.parser")

    # Header ophalen
    headers = [
        h.text.strip() for h in soup.select("div.tableHeader div.column")
    ]

    # Data ophalen
    rows = soup.find_all("div", class_="row lv-0 yf-t22klz")
    data = []
    for row in rows:
        title_div = row.find("div", class_="rowTitle")
        title = title_div.text.strip() if title_div else "?"
        value_cells = [
            div for div in row.find_all("div")
            if "column" in div.get("class", []) and "yf-t22klz" in div.get("class", []) and "sticky" not in div.get("class", [])
        ]
        values = [v.text.strip() for v in value_cells]
        data.append([title] + values)

    df = pd.DataFrame(data, columns=["Breakdown"] + headers[1:])  # Eerste kolom = Breakdown
    return df
