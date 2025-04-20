import requests
from bs4 import BeautifulSoup
import pandas as pd

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

        return matchup_df

    except Exception as e:
        print(">>> ERROR scraping matchups:", e)
        import traceback
        traceback.print_exc()
        return pd.DataFrame(columns=["player", "pitcher"])
