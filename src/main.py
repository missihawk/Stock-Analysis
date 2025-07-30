from yf_driver import start_driver, open_yf, close_driver
from fetch.financials import fetch_yahoo_statement

driver = start_driver(True)
open_yf(driver)  # cookies accepteren

for kind in ["financials", "balance-sheet", "cash-flow"]:
    df = fetch_yahoo_statement(driver, "BFIT.AS", kind, False)
    print(f"\n=== {kind.upper()} ===\n", df)

close_driver(driver)
