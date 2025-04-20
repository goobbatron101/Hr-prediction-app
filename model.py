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
        tb = traceback.format_exc()
        print(">>> FATAL ERROR in predict_home_runs():")
        print(tb)

        # Return minimal fallback to keep Streamlit running
        return pd.DataFrame({
            "player": ["error"],
            "pitcher": ["see log"],
            "slg": [None],
            "iso": [None],
            "hr": [None]
        })