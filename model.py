print(">>> model.py import test starting...")

try:
    from data_loader import (
        load_batter_features,
        load_pitcher_features,
        get_today_matchups
    )

    print(">>> Successfully imported data_loader functions.")

    # Call each one safely
    batters = load_batter_features()
    pitchers = load_pitcher_features()
    matchups = get_today_matchups()

    print(">>> All data functions executed.")
    print(">>> Batters:", len(batters))
    print(">>> Pitchers:", len(pitchers))
    print(">>> Matchups:", len(matchups))

    def predict_home_runs(df_input):
        return batters.head(5)  # dummy

except Exception as e:
    import traceback
    print(">>> ERROR during model.py testing:")
    traceback.print_exc()
    raise e
