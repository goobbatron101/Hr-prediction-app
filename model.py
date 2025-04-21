import pandas as pd
import numpy as np

def predict_home_runs(df_input=None):
    try:
        print(">>> Running predict_home_runs...")

        from data_loader import load_batter_features, get_today_matchups

        # Optional: Load trained model
        try:
            import joblib
            model = joblib.load("models/hr_model.pkl")
            print(">>> Model loaded.")
            use_real_model = True
        except:
            print(">>> Could not load model, using fallback scoring.")
            model = None
            use_real_model = False

        # Load data
        batters = load_batter_features()  # Must include a 'team' column (real MLB team)
        matchups = get_today_matchups()   # From MLB API — real matchups

        if batters.empty or matchups.empty:
            print(">>> No data available.")
            return pd.DataFrame({"player": ["No data"], "pitcher": [None]})

        # Filter batters to only those whose teams are playing today
        playing_teams = matchups['team'].unique().tolist()
        batters = batters[batters['team'].isin(playing_teams)]

        if batters.empty:
            print(">>> No batters from teams in today's matchups.")
            return pd.DataFrame({"player": ["No batters for today's slate"], "pitcher": [None]})

        # Merge with matchups to get opposing pitcher
        df = pd.merge(batters, matchups, on='team', how='left')

        # Features used for model or fallback
        features = ["slg", "iso", "hr"]

        if use_real_model and all(f in df.columns for f in features):
            df_model = df.dropna(subset=features)
            X = df_model[features]
            df.loc[df_model.index, "hr_prob"] = np.round(model.predict_proba(X)[:, 1], 3)
        else:
            df["hr_prob"] = (
                0.15 * df["slg"] +
                0.5 * df["iso"] +
                0.01 * df["hr"]
            ).clip(0, 1).round(3)

        # Return the columns used in Streamlit app
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
