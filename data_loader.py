from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import traceback
import requests
from bs4 import BeautifulSoup
from pybaseball import batting_stats, pitching_stats

def load_batter_features():
    try:
        print(">>> loading batters...")
        from pybaseball import batting_stats
        import numpy as np
        import pandas as pd

        df = batting_stats(2024, qual=20)

        df = df.rename(columns={
            'Name': 'player',
            'SLG': 'slg',
            'ISO': 'iso',
            'HR/FB': 'hr_fb',
            'BB%': 'bb_rate',
            'K%': 'k_rate',
            'PA': 'pa',
            'HR': 'hr'
        })

        df = df[['player', 'slg', 'iso', 'hr_fb', 'bb_rate', 'k_rate', 'pa', 'hr']]
        df.dropna(inplace=True)

        df['park_factor'] = np.random.normal(1.0, 0.1, len(df))
        df['wind'] = np.random.normal(5, 3, len(df))
        df['temperature'] = np.random.normal(75, 10, len(df))
        df['humidity'] = np.random.normal(50, 15, len(df))

        print(">>> loaded batters:", len(df))
        return df

    except Exception as e:
        import traceback
        tb = traceback.format_exc()

        # Save to CSV as a visible crash marker
        pd.DataFrame({"error": [str(e)], "traceback": [tb]}).to_csv("error_log.csv", index=False)

        print(">>> ERROR loading batters:")
        print(tb)
        raise e
# ----------------------------------
# Load Pitchers
# ----------------------------------
def load_pitcher_features():
    try:
        print(">>> Loading pitchers...")
        df = pitching_stats(2024, qual=20)

        df = df.rename(columns={
            'Name': 'pitcher',
            'ERA': 'era',
            'FIP': 'fip',
            'HR/9': 'hr9',
            'K%': 'k_rate',
            'BB%': 'bb_rate'
        })

        df = df[['pitcher', 'era', 'fip', 'hr9', 'k_rate', 'bb_rate']]
        df.dropna(inplace=True)

        print(">>> Pitchers loaded:", len(df))
        return df.reset_index(drop=True)

    except Exception as e:
        print(">>> ERROR loading pitchers:", e)
        traceback.print_exc()
        return pd.DataFrame()

import requests
import pandas as pd
from datetime import datetime

def get_today_matchups():
    try:
        print(">>> Fetching MLB matchups from statsapi...")


# Step 1: Try today, fallback to tomorrow if needed
today = datetime.today()
today_str = today.strftime('%Y-%m-%d')

url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today_str}"
response = requests.get(url).json()

games = response.get("dates", [])
if not games:
    # Fallback to tomorrow
    tomorrow = (today + timedelta(days=1)).strftime('%Y-%m-%d')
    print(f">>> No games found for {today_str}, trying {tomorrow}...")
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={tomorrow}"
    response = requests.get(url).json()

        # Get today's MLB schedule
        url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}"
        schedule_response = requests.get(url).json()

        matchups = []

        for date_info in schedule_response.get("dates", []):
            for game in date_info.get("games", []):
                try:
                    away_team = game['teams']['away']['team']['name']
                    home_team = game['teams']['home']['team']['name']

                    away_pitcher = game['teams']['away'].get('probablePitcher', {}).get('fullName')
                    home_pitcher = game['teams']['home'].get('probablePitcher', {}).get('fullName')

                    if away_pitcher:
                        matchups.append({
                            "team": away_team,
                            "pitcher": away_pitcher
                        })

                    if home_pitcher:
                        matchups.append({
                            "team": home_team,
                            "pitcher": home_pitcher
                        })

                except Exception as e:
                    print(">>> Skipping one game due to error:", e)

        matchup_df = pd.DataFrame(matchups)
        print(">>> Matchups found:", len(matchup_df))
if matchup_df.empty:
    print(">>> Using test fallback matchups...")
    matchup_df = pd.DataFrame([
        {"team": "Atlanta Braves", "pitcher": "Chris Sale"},
        {"team": "Los Angeles Dodgers", "pitcher": "Yoshinobu Yamamoto"}
    ])
        return matchup_df

    except Exception as e:
        print(">>> ERROR fetching MLB matchups:", e)
        return pd.DataFrame(columns=["team", "pitcher"])
