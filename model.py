import pandas as pd
import numpy as np

def predict_home_runs(df_input=None):
    try:
        print(">>> Running predict_home_runs...")

        from data_loader import load_batter_features, get_today_matchups

        # Load data
        batters = load_batter_features()
        matchups = get_today_matchups()

        if batters.empty or matchups.empty:
            print(">>> No data available.")
            return pd.DataFrame({"player": ["No data"], "pitcher": [None]})

        # Simulate team assignment for batters
        teams = matchups['team'].unique().tolist()
        if len(teams) < 1:
            print(">>> No teams to assign.")
            return pd.DataFrame({"player": ["No matchups available"], "pitcher": [None]})

        batters = batters.head(20)  # Limit for testing/demo
        batters['team'] = np.random.choice(teams, size=len(batters))

        # Merge with matchups to assign pitchers
        df = pd.merge(batters, matchups, on='team', how='left')

        # Step: Add HR Probability (mock model)
        df["hr_prob"] = (
            0.15 * df["slg"] +
            0.5 * df["iso"] +
            0.01 * df["hr"]
        ).clip(0, 1).round(3)

        # Return final data for display
        return df[['player', 'team', 'pitcher', 'slg', 'iso', 'hr', 'hr_prob']]

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(">>> ERROR in predict_home_runs:")
        print(tb)
        return pd.DataFrame({
            "player": ["Error occurred"],
            "pitcher": [None],
            "team": [None],
            "slg": [None],
            "iso": [None],
            "hr": [None],
            "hr_prob": [None]
        })
