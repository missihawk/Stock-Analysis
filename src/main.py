from yf_driver import start_driver, open_yf, close_driver
from fetch.financials import fetch_yf_statement
from storage.local_data import load_data, merge_statement_data, save_data
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

driver = start_driver(True)
open_yf(driver)  # cookies accepteren

for ticker in ["AXS.AS", "ACOMO.AS", "ALFEN.AS", "BFIT.AS", "BMW3.DE", "DTE.DE", "FNTN.DE", "BOSS.DE", "KENDR.AS", "MBG.DE", "NEDAP.AS", "SLIGR.AS", "TKA.DE", "VLK.AS", "VOW3.DE", "ZAL.DE"]:
    logging.info(f"Start processing: {ticker}")
    start_time = time.perf_counter()
    
    try:
        data = load_data(ticker)

        for report_type in ["FY", "Q"]:
            for statement_type in ["financials", "balance-sheet", "cash-flow"]:
                df = fetch_yf_statement(driver, ticker, statement_type, report_type)
                data = merge_statement_data(data, df, statement_type, report_type)

        save_data(ticker, data)
    except Exception as e:
        logging.error(f"Error while processing {ticker}: {e}")

    end_time = time.perf_counter()
    logging.info(f"Finished {ticker} in {end_time - start_time:.2f} seconds\n")

close_driver(driver)