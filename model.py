print(">>> Importing model.py...")

import pandas as pd
import numpy as np
from data_loader import load_batter_features, load_pitcher_features

def predict_home_runs(df_input=None):
    print(">>> Loading batters and pitchers...")
    batters = load_batter_features()
    pitchers = load_pitcher_features()

    # Randomly assign a pitcher to each batter (temporary)
    np.random.seed(42)
    pitcher_sample = pitchers.sample(n=len(batters), replace=True).reset_index(drop=True)

    df = pd.concat([batters.reset_index(drop=True), pitcher_sample], axis=1)
    return df[['player', 'pitcher', 'slg', 'era', 'hr9']].head(15)
