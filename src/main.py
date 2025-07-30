from yf_driver import start_driver, open_yf, close_driver
from fetch.financials import fetch_yf_statement
from storage.local_data import load_data, merge_statement_data, save_data

driver = start_driver(True)
open_yf(driver)  # cookies accepteren

for ticker in ["AXS.AS", "ACOMO.AS", "ALFEN.AS", "BFIT.AS", "BMW3.DE", "DTE.DE", "FNTN.DE", "BOSS.DE", "KENDR.AS", "MBG.DE", "NEDAP.AS", "SLIGR.AS", "TKA.DE", "VLK.AS", "VOW3.DE", "ZAL.DE"]:
    data = load_data(ticker)

    for report_type in ["FY", "Q"]:
        for statement_type in ["financials", "balance-sheet", "cash-flow"]:
            df = fetch_yf_statement(driver, ticker, statement_type, report_type)
            data = merge_statement_data(data, df, statement_type, report_type)

    save_data(ticker, data)

close_driver(driver)
