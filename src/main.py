from yf_driver import start_driver, open_yf, close_driver
from fetch.financials import fetch_financials

driver = start_driver(headless=True)
open_yf(driver)  # cookies accepteren

df = fetch_financials(driver, "BFIT.AS", save_html=True)
print(df)

close_driver(driver)
