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
        batters = load_batter_features()
        matchups = get_today_matchups()

        if batters.empty or matchups.empty:
            return pd.DataFrame({"player": ["No data"], "pitcher": [None]})

        # Match only teams playing today
        playing_teams = matchups['team'].unique().tolist()
        batters = batters[batters['team'].isin(playing_teams)]

        if batters.empty:
            return pd.DataFrame({"player": ["No batters for today's slate"], "pitcher": [None]})

        # Merge with matchups to get opposing pitcher
        df = pd.merge(batters, matchups, on='team', how='left')

        # Updated features based on Savant CSV
        features = ["xhr", "xslg", "ev", "la", "hr_pa"]

        if use_real_model and all(f in df.columns for f in features):
            df_model = df.dropna(subset=features)
            X = df_model[features]
            df.loc[df_model.index, "hr_prob"] = np.round(model.predict_proba(X)[:, 1], 3)
        else:
            df["hr_prob"] = (
                0.15 * df["xslg"] +
                0.15 * df["xhr"] +
                0.1 * df["ev"] +
                0.05 * df["la"] +
                0.05 * df["hr_pa"]
            ).clip(0, 1).round(3)

        # Return columns your Streamlit app expects (adjust labels in app.py if needed)
        return df[['player', 'team', 'pitcher', 'xhr', 'xslg', 'ev', 'la', 'hr', 'hr_prob']]

    except Exception as e:
        import traceback
        print(">>> ERROR in predict_home_runs:")
        print(traceback.format_exc())
        return pd.DataFrame()