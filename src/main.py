from yf_driver import start_driver, open_yf, close_driver
from fetch.financials import fetch_yf_statement
from storage.local_data import load_data, merge_statement_data, save_data

driver = start_driver(True)
open_yf(driver)  # cookies accepteren

ticker = "BFIT.AS"
report_type = "Q"

df_income = fetch_yf_statement(driver, ticker, "financials", report_type)
df_cashflow = fetch_yf_statement(driver, ticker, "cash-flow", report_type)
df_balance = fetch_yf_statement(driver, ticker, "balance-sheet", report_type)
data = load_data(ticker)
data = merge_statement_data(data, df_income, "income", report_type)
data = merge_statement_data(data, df_cashflow, "cashflow", report_type)
data = merge_statement_data(data, df_balance, "balance", report_type)

save_data(ticker, data)

close_driver(driver)
