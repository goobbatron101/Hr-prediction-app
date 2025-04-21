import pandas as pd

def predict_home_runs(df_input=None):
    try:
        print(">>> Running predict_home_runs...")

        from data_loader import load_batter_features, get_today_matchups
        import numpy as np

        batters = load_batter_features()
        matchups = get_today_matchups()

        print(">>> Batters shape:", batters.shape)
        print(">>> Matchups shape:", matchups.shape)

        if batters.empty:
            print(">>> No batters loaded.")
            return pd.DataFrame({"player": ["No batters found"], "pitcher": [None]})

        if matchups.empty:
            print(">>> No matchups found.")
            # Just return batters with a placeholder pitcher
            return pd.DataFrame({
                "player": batters["player"].head(),
                "pitcher": ["TBD"] * len(batters.head())
            })

        batters['team'] = np.random.choice(matchups['team'].unique(), size=len(batters))
        df = pd.merge(batters, matchups, on='team', how='left')

        print(">>> Final merged shape:", df.shape)
        return df[['player', 'pitcher', 'team']].head(10)

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(">>> ERROR in predict_home_runs:")
        print(tb)
        return pd.DataFrame({
            "player": ["Error occurred"],
            "pitcher": [None],
            "team": [None]
        })