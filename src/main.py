from yf_driver import start_driver, open_yf, close_driver
from fetch.financials import fetch_yf_statement
from storage.local_data import load_data, merge_statement_data, save_data

driver = start_driver(True)
open_yf(driver)  # cookies accepteren

ticker = "BFIT.AS"
report_type = "FY"

df_income = fetch_yf_statement(driver, ticker, "financials", report_type)
data = load_data(ticker)
data = merge_statement_data(data, df_income, report_type)
save_data(ticker, data)

close_driver(driver)
