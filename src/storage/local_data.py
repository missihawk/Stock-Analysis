import os
import pickle
import pandas as pd

def load_data(ticker: str, folder="data") -> dict:
    path = os.path.join(folder, f"{ticker.upper()}.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return {}

def save_data(ticker: str, data: dict, folder="data"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{ticker.upper()}.pkl")
    with open(path, "wb") as f:
        pickle.dump(data, f)

def merge_statement_data(
    existing_data: dict,
    new_df,
    statement_type: str,
    report_type: str  # e.g. 'FY' for annual, 'Q' for quarterly
) -> dict:
    """
    Merge a financial statement into the existing_data structure.

    Args:
        existing_data (dict): The current dataset to update.
        new_df (pd.DataFrame): A financial statement dataframe from Yahoo.
        statement_type (str): Type of statement ('income', 'cashflow', 'balance').
        report_type (str): Reporting period ('FY' for yearly, 'Q' for quarterly).

    Returns:
        dict: Updated dataset with the merged statement.
    """

    # Prepare root level if needed
    if report_type not in existing_data:
        existing_data[report_type] = {}

    # Drop TTM (Trailing Twelve Months) row if present
    if "TTM" in new_df.columns:
        new_df = new_df.drop(columns=["TTM"])

    # Convert format: set 'Breakdown' as index so each column becomes a report date
    new_df = new_df.set_index("Breakdown").transpose()

    # Reset index to get a column called 'date'
    new_df.reset_index(inplace=True)
    new_df.rename(columns={"index": "date"}, inplace=True)

    # Convert date strings to proper datetime (and back to ISO string format)
    new_df["date"] = pd.to_datetime(new_df["date"], errors="coerce").dt.strftime("%Y-%m-%d")

    for _, row in new_df.iterrows():
        date = row["date"]

        if pd.isna(date):
            continue  # skip invalid or NaT dates

        # Create date entry if not present
        if date not in existing_data[report_type]:
            existing_data[report_type][date] = {}

        # Insert statement_type data
        existing_data[report_type][date][statement_type] = {}

        for col in new_df.columns:
            if col == "date":
                continue

            val = row[col]

            # Optional: convert numbers with commas to floats
            if isinstance(val, str):
                try:
                    val = float(val.replace(",", ""))
                except ValueError:
                    pass

            existing_data[report_type][date][statement_type][col] = val

    return existing_data
