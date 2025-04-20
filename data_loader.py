import pandas as pd
import numpy as np
import traceback
import requests
from bs4 import BeautifulSoup
from pybaseball import batting_stats, pitching_stats

# ----------------------------------
# Load Batters with Simulated Weather & Park
# ----------------------------------
def load_batter_features():
    try:
        print(">>> Loading batters...")
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

        # Add simulated park/weather values
        df['park_factor'] = np.random.normal(1.0, 0.1, len(df))
        df['wind'] = np.random.normal(5, 3, len(df))
        df['temperature'] = np.random.normal(75, 10, len(df))
        df['humidity'] = np.random.normal(50, 15, len(df))
print(">>> FINAL batters df shape:", df.shape)
        print(">>> Batters loaded:", len(df))
        return df.reset_index(drop=True)

    except Exception as e:
        print(">>> ERROR loading batters:", e)
        traceback.print_exc()
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

# ----------------------------------
# Scrape Rotowire Matchups
# ----------------------------------
def get_today_matchups():
    try:
        print(">>> Scraping Rotowire matchups...")
        url = "https://www.rotowire.com/baseball/daily-lineups.php"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        matchups = []

        teams = soup.find_all("div", class_="lineup is-expected")
        for team in teams:
            pitcher_tag = team.find("span", class_="lineup__note")
            if not pitcher_tag:
                continue

            pitcher_name = (
                pitcher_tag.text.strip()
                .replace("Probable Pitcher: ", "")
                .split(" ")[0:2]
            )
            pitcher_name = " ".join(pitcher_name)

            batters = team.find_all("div", class_="lineup__player")
            for b in batters:
                batter_name = b.text.strip().split(" ")[0:2]
                batter_name = " ".join(batter_name)
                matchups.append({"player": batter_name, "pitcher": pitcher_name})

        matchup_df = pd.DataFrame(matchups)
        print(">>> Matchups preview:")
        print(matchup_df.head())
print(">>> FINAL matchups df shape:", matchup_df.shape)
        return matchup_df

    except Exception as e:
        print(">>> ERROR scraping matchups:", e)
        traceback.print_exc()
        return pd.DataFrame(columns=["player", "pitcher"])
