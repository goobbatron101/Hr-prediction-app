import pandas as pd
import numpy as np

def predict_home_runs(df_input=None):
    try:
        print(">>> Running predict_home_runs...")

        from data_loader import load_batter_features, get_today_matchups

        batters = load_batter_features()
        matchups = get_today_matchups()

        if batters.empty or matchups.empty:
            print(">>> No data available.")
            return pd.DataFrame({"player": ["No data"], "pitcher": [None]})

        # Assign 50% of batters to each matchup team
        teams = matchups['team'].unique().tolist()
        if len(teams) < 2:
            print(">>> Not enough teams to assign.")
            return pd.DataFrame({"player": ["Fallback team match failed"], "pitcher": [None]})

        batters = batters.head(20)  # just 20 batters to test
        batters['team'] = np.random.choice(teams, size=len(batters))

        # Merge batters with matchup pitchers by team
        df = pd.merge(batters, matchups, on='team', how='left')

        return df[['player', 'team', 'pitcher', 'slg', 'iso', 'hr']]

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