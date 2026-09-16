from pathlib import Path
import pandas as pd
import os

class Olist:
    def get_data(self):
        csv_path = Path("~/.lewagon/olist/data/csv").expanduser()
        file_names = [f.name for f in csv_path.iterdir() if f.name.endswith('.csv')]

        key_names = [
            f.name.replace('olist_', '').replace('_dataset.csv', '').replace('.csv', '')
            for f in csv_path.iterdir() if f.name.endswith('.csv')
        ]

        data = {}
        for key, file in zip(key_names, file_names):
            data[key] = pd.read_csv(csv_path / file)

        return data
