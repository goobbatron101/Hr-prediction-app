print(">>> Importing model.py...")

try:
    import pandas as pd
    from data_loader import (
        load_batter_features,
        get_today_matchups
    )
except Exception as e:
    import traceback
    print(">>> ERROR in model.py during import:")
    traceback.print_exc()
    raise e

def predict_home_runs(df_input=None):
    print(">>> Model loaded — basic test output")
    return pd.DataFrame({"player": ["Test"], "HR_Probability": [0.5]})
    
    batters = load_batter_features()
    matchups = get_today_matchups()

    if matchups.empty:
        print(">>> No matchups found — returning batters only.")
        return batters[['player']].head(10)

    # Merge real matchups with batter data
    df = pd.merge(batters, matchups, on='player', how='inner')
print(">>> Matchups preview:")
print(matchups[:5])
    return df[['player', 'pitcher', 'slg', 'iso', 'hr_fb', 'bb_rate', 'k_rate', 'pa', 'hr']]