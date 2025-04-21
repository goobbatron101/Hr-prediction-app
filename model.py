import pandas as pd
import numpy as np

def predict_home_runs(df_input=None):
    try:
        print(">>> Running predict_home_runs...")

        from data_loader import load_batter_features, get_today_matchups

        # Optional: load a trained model (commented if not available yet)
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
        batters = load_batter_features()
        matchups = get_today_matchups()

        if batters.empty or matchups.empty:
            print(">>> No data available.")
            return pd.DataFrame({"player": ["No data"], "pitcher": [None]})

        # Simulate team assignment
        teams = matchups['team'].unique().tolist()
        if len(teams) < 1:
            return pd.DataFrame({"player": ["No matchups available"], "pitcher": [None]})

        batters = batters.head(20)
        batters['team'] = np.random.choice(teams, size=len(batters))

        # Merge with matchups
        df = pd.merge(batters, matchups, on='team', how='left')

        # Features to use for model
        features = ["slg", "iso", "hr"]  # Example — update with your real model's input features

        if use_real_model and all(f in df.columns for f in features):
            # Drop rows with missing values in key features
            df_model = df.dropna(subset=features)
            X = df_model[features]

            # Predict HR probability
            hr_probs = model.predict_proba(X)[:, 1]
            df.loc[df_model.index, "hr_prob"] = np.round(hr_probs, 3)
        else:
            # Fallback mock scoring
            df["hr_prob"] = (
                0.15 * df["slg"] +
                0.5 * df["iso"] +
                0.01 * df["hr"]
            ).clip(0, 1).round(3)

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
