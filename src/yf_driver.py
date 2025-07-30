from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...")
    options.add_argument("--log-level=3")

    # Zorg dat logging niet in de console komt, maar in chrome_debug.log
    service = Service(log_path="chrome_debug.log")
    driver = webdriver.Chrome(options=options, service=service)
    driver.implicitly_wait(3)
    return driver

def open_yf(driver: webdriver.Chrome) -> None:
    url = "https://finance.yahoo.com/"
    driver.get(url)

    try:
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.NAME, "agree"))
        )
        accept_button.click()
        print("Cookies geaccepteerd.")
    except Exception:
        print("Geen cookiebanner gevonden of al geaccepteerd.")

def close_driver(driver: webdriver.Chrome) -> None:
    try:
        driver.quit()
        print("Driver afgesloten.")
    except Exception as e:
        print(f"Fout bij afsluiten van driver: {e}")
