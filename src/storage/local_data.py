import os
import pickle
from datetime import datetime

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

def merge_statement_data(existing_data: dict, new_df, report_type: str) -> dict:
    if report_type not in existing_data:
        existing_data[report_type] = {}

    # Zet eerste kolom als index, transposeer, reset
    new_df.set_index("Breakdown", inplace=True)
    df = new_df.transpose()
    df.reset_index(inplace=True)
    df.rename(columns={"index": "date"}, inplace=True)

    # Filter ongeldige of ongewenste datums zoals "TTM"
    df = df[df["date"].apply(lambda x: x != "TTM" and isinstance(x, str) and len(x) >= 4)]

    for _, row in df.iterrows():
        raw_date = row["date"]
        try:
            date_obj = datetime.strptime(raw_date, "%m/%d/%Y")  # of "%Y-%m-%d"
        except ValueError:
            try:
                date_obj = datetime.strptime(raw_date, "%Y-%m-%d")
            except ValueError:
                print(f"⚠️ Ongeldige datum '{raw_date}' overgeslagen")
                continue

        # Zet als string (of gebruik date_obj als je datums wil)
        date = date_obj.strftime("%Y-%m-%d")

        # Dubbelcheck op bestaand datapunt
        if date not in existing_data[report_type]:
            existing_data[report_type][date] = {}

        for col in row.index:
            if col == "date":
                continue

            # Optioneel: getal omzetten van string met komma naar float
            val = row[col]
            if isinstance(val, str):
                val = val.replace(",", "")
                try:
                    val = float(val)
                except ValueError:
                    pass

            existing_data[report_type][date][col] = val

    return existing_data
