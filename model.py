import pandas as pd

def predict_home_runs(df_input=None):
    try:
        print(">>> Running predict_home_runs...")

        from data_loader import load_batter_features, load_pitcher_features, get_today_matchups
        import numpy as np

        batters = load_batter_features()
        pitchers = load_pitcher_features()
        matchups = get_today_matchups()

        print(">>> Batters shape:", batters.shape)
        print(">>> Matchups shape:", matchups.shape)

        if batters.empty or matchups.empty:
            print(">>> One of the inputs is empty.")
            return pd.DataFrame({"player": ["No data"], "pitcher": [None], "team": [None]})

        # Simulate team for now
        batters['team'] = np.random.choice(matchups['team'].unique(), size=len(batters))

        # Merge with matchups to assign pitcher
        df = pd.merge(batters, matchups, on='team', how='left')

        print(">>> Final merged shape:", df.shape)
        return df[['player', 'team', 'pitcher', 'slg', 'iso', 'hr']]

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(">>> ERROR in predict_home_runs:")
        print(tb)
        return pd.DataFrame({
            "player": ["Error occurred"],
            "team": [None],
            "pitcher": [None],
            "slg": [None],
            "iso": [None],
            "hr": [None]
        })