print(">>> Importing model.py...")

import pandas as pd
from data_loader import load_batter_features

def predict_home_runs(df_input=None):
    print(">>> Loading real batter data...")
    batters = load_batter_features()
    return batters.head(10)
