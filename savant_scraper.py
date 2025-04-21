import pandas as pd
import requests
from io import StringIO

def download_savant_batter_stats(season=2025, min_pa=10):
    print(">>> Downloading Baseball Savant leaderboard...")

    # Savant CSV export URL (Statcast Batting Leaderboard)
    url = (
        f"https://baseballsavant.mlb.com/leaderboard/statcast-rates?"
        f"type=batter&year={season}&position=&team=&min={min_pa}&csv=true"
    )

    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch CSV. Status code: {response.status_code}")

        # Parse CSV into DataFrame
        df = pd.read_csv(StringIO(response.text))

        # Select relevant columns and rename
        df = df.rename(columns={
            "player_name": "player",
            "team": "team",
            "xHR": "xhr",
            "xSLG": "xslg",
            "avg_hit_speed": "ev",
            "avg_launch_angle": "la",
            "PA": "pa",
            "HR": "hr"
        })

        df["hr_pa"] = (df["hr"] / df["pa"]).round(4)
        df = df[["player", "team", "xhr", "xslg", "ev", "la", "hr", "pa", "hr_pa"]]
        df.to_csv("data/savant_batters_2025.csv", index=False)

        print(f">>> Saved {len(df)} players to data/savant_batters_2025.csv")
        return df

    except Exception as e:
        import traceback
        print(">>> Error while fetching Savant data:")
        print(traceback.format_exc())
        return pd.DataFrame()
