from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import traceback
import requests
from bs4 import BeautifulSoup
from pybaseball import batting_stats, pitching_stats

import pandas as pd
import requests

def load_batter_features(season=2025, min_pa=20):
    print(">>> Fetching 2025 batter stats from MLB Stats API...")

    # MLB Stats API endpoint for batter stats
    url = (
        f"https://statsapi.mlb.com/api/v1/stats"
        f"?stats=season&group=hitting&season={season}&gameType=R&limit=10000"
    )

    try:
        response = requests.get(url)
        data = response.json()

        rows = []
        for player in data.get("stats", [])[0].get("splits", []):
            person = player["player"]
            stat = player["stat"]
            team = player.get("team", {}).get("name", "Unknown")

            # Filter by min plate appearances
            pa = int(stat.get("plateAppearances", 0))
            if pa < min_pa:
                continue

            # Calculate ISO = SLG - AVG
            avg = float(stat.get("avg", 0))
            slg = float(stat.get("sluggingPercentage", 0))
            iso = round(slg - avg, 3)

            rows.append({
                "player": person["fullName"],
                "team": team,
                "slg": slg,
                "iso": iso,
                "hr": int(stat.get("homeRuns", 0)),
            })

        df = pd.DataFrame(rows)
        print(f">>> Loaded {len(df)} batters from MLB Stats API.")
        return df

    except Exception as e:
        print(">>> Failed to load batter stats.")
        import traceback
        print(traceback.format_exc())
        return pd.DataFrame()
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
from datetime import datetime, timedelta

def get_today_matchups():
    print(">>> Fetching MLB matchups from statsapi...")

    try:
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

        matchups = []

        for date_info in response.get("dates", []):
            for game in date_info.get("games", []):
                try:
                    away_team = game['teams']['away']['team']['name']
                    home_team = game['teams']['home']['team']['name']

                    away_pitcher = game['teams']['away'].get('probablePitcher', {}).get('fullName')
                    home_pitcher = game['teams']['home'].get('probablePitcher', {}).get('fullName')

                    if away_pitcher:
                        matchups.append({"team": away_team, "pitcher": away_pitcher})
                    if home_pitcher:
                        matchups.append({"team": home_team, "pitcher": home_pitcher})
                except Exception as inner:
                    print(">>> Skipping one game due to error:", inner)

        matchup_df = pd.DataFrame(matchups)

        if matchup_df.empty:
            print(">>> Using test fallback matchups...")
            matchup_df = pd.DataFrame([
                {"team": "Atlanta Braves", "pitcher": "Chris Sale"},
                {"team": "Los Angeles Dodgers", "pitcher": "Yoshinobu Yamamoto"}
            ])

        print(">>> Matchups preview:")
        print(matchup_df.head())

        return matchup_df

    except Exception as e:
        print(">>> ERROR fetching MLB matchups:", e)
        return pd.DataFrame(columns=["team", "pitcher"])
