print(">>> model.py loaded (safe fallback version)")

import pandas as pd

def predict_home_runs(df_input=None):
    try:
        print(">>> Running predict_home_runs...")
        from data_loader import load_batter_features, get_today_matchups

        batters = load_batter_features()
        matchups = get_today_matchups()

        print(">>> Sample batters:", batters['player'].head().tolist())
        print(">>> Sample matchups:", matchups.head())

        df = pd.merge(batters, matchups, on='player', how='inner')
        return df[['player', 'pitcher', 'slg', 'iso', 'hr']]

    except Exception as e:
        import traceback
        print(">>> ERROR in predict_home_runs:")
        traceback.print_exc()
        return pd.DataFrame({"error": ["Something went wrong in predict_home_runs()"]})
