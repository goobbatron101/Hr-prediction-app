import pandas as pd

def predict_home_runs(df_input=None):
    try:
        print(">>> Running predict_home_runs...")

        from data_loader import get_today_matchups

        matchups = get_today_matchups()

        print(">>> Matchups DataFrame:")
        print(matchups.head(10))

        if matchups.empty:
            print(">>> No matchups found.")
            return pd.DataFrame({"message": ["No matchups returned"]})

        return matchups[['team', 'pitcher']].head(10)

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(">>> ERROR in predict_home_runs:")
        print(tb)
        return pd.DataFrame({
            "message": ["Error occurred"],
            "traceback": [tb]
        })