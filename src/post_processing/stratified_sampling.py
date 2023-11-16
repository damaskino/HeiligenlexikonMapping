import pandas as pd

df = pd.read_json(
    "/kaggle/input/heiligenlexikon-json/parsed_heiligenlexikon_v1.json", orient="index"
)
