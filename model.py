print(">>> Importing model.py...")

import pandas as pd
from data_loader import load_batter_features, get_today_matchups

def predict_home_runs(df_input=None):
    print(">>> Loading batters and real matchups...")
    
    batters = load_batter_features()
    matchups = get_today_matchups()

    if matchups.empty:
        print(">>> No matchups found — returning batters only.")
        return batters[['player']].head(10)

    # Merge real matchups with batter data
    df = pd.merge(batters, matchups, on='player', how='inner')

    return df[['player', 'pitcher', 'slg', 'iso', 'hr_fb', 'bb_rate', 'k_rate', 'pa', 'hr']]