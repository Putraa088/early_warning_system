import os
import json
import datetime
import pandas as pd

class DataStorageController:

    def __init__(self):
        self.daily_path = "data_harian"
        self.monthly_path = "data_bulanan"

        os.makedirs(self.daily_path, exist_ok=True)
        os.makedirs(self.monthly_path, exist_ok=True)

    # ============= DAILY DATA (FORMAT A) =============
    def save_daily(self, data):
        today = datetime.date.today()
        filename = os.path.join(self.daily_path, f"{today}.json")

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        return filename

    def read_daily(self, date: str):
        filename = os.path.join(self.daily_path, f"{date}.json")
        if not os.path.exists(filename):
            return None

        with open(filename, "r") as f:
            return json.load(f)

    # ============= MONTHLY DATA (FORMAT C) =============
    def update_monthly(self, data):
        today = datetime.date.today()
        month_str = today.strftime("%Y-%m")
        filename = os.path.join(self.monthly_path, f"{month_str}.csv")

        df_new = pd.DataFrame([data])

        if os.path.exists(filename):
            df_old = pd.read_csv(filename)
            df_all = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_all = df_new

        df_all.to_csv(filename, index=False)
        return filename

    def read_monthly(self, year_month: str):
        filename = os.path.join(self.monthly_path, f"{year_month}.csv")
        if not os.path.exists(filename):
            return None
        return pd.read_csv(filename)
