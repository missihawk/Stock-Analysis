# fetch/financials.py
from bs4 import BeautifulSoup
import pandas as pd
import time, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_yahoo_statement(driver, ticker: str, statement_type: str, save_html: bool = False) -> pd.DataFrame:
    """
    statement_type: one of "financials", "balance-sheet", "cash-flow"
    """
    url = f"https://finance.yahoo.com/quote/{ticker}/{statement_type}"
    driver.get(url)

    wait = WebDriverWait(driver, 20)

    # Wacht op table container
    try:
        tab = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.tableContainer.yf-9ft13")))
        tab.click()
    except:
        print(f"[{ticker.upper()}] ⚠️ Tabel niet gevonden.")
        return pd.DataFrame()

    # HTML opslaan (optioneel)
    html = driver.page_source
    if save_html:
        timestamp = time.strftime("%Y-%m-%d_%H-%M")
        os.makedirs(f"html/{ticker}", exist_ok=True)
        with open(f"html/{ticker}/{timestamp}.html", "w", encoding="utf-8") as f:
            f.write(html)

    soup = BeautifulSoup(html, "html.parser")

    # Header ophalen
    header_divs = soup.select("div.tableHeader div.column")
    headers = [h.text.strip() for h in header_divs]

    # ✅ CSS class hangt af van het type statement
    row_class = {
        "financials": "yf-t22klz",
        "balance-sheet": "yf-t22klz",
        "cash-flow": "yf-t22klz"
    }.get(statement_type)

    # Data ophalen
    rows = soup.find_all("div", class_=f"row lv-0 {row_class}")
    records = []

    for row in rows:
        title_div = row.find("div", class_="rowTitle")
        title = title_div.text.strip() if title_div else "?"

        data_divs = [
            div for div in row.find_all("div")
            if "column" in div.get("class", []) and 
                row_class in div.get("class", []) and 
                "sticky" not in div.get("class", [])
        ]

        values = [v.text.strip() for v in data_divs]
        records.append([title] + values)

    df = pd.DataFrame(records, columns=["Breakdown"] + headers[1:])
    return df
