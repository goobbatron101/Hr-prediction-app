print(">>> Importing model.py...")

import pandas as pd

def predict_home_runs(df_input):
    print(">>> predict_home_runs() called.")
    return pd.DataFrame({
        "player": ["Test Player"],
        "HR_Probability": [0.25],
        "Recommendation": ["Watchlist"]
    })
