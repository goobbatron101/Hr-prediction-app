from pybaseball import batting_stats
import pandas as pd
import traceback
print(">>> Running data_loader.py")
def load_batter_features():
    try:
        # Pull 2024 season batter stats
        df = batting_stats(2024, qual=20)
print(">>> Loading batters...")

        # Select and rename key features
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

        features = ['player', 'slg', 'iso', 'hr_fb', 'bb_rate', 'k_rate', 'pa', 'hr']
        df = df[features]

        # Drop any missing values
        df.dropna(inplace=True)

        return df.reset_index(drop=True)
from pybaseball import pitching_stats

def load_pitcher_features():
    try:
        # Load pitcher stats for 2024 season
        df = pitching_stats(2024, qual=20)

print(">>> Loading pitchers...")
        # Select relevant columns and rename for consistency
        df = df.rename(columns={
            'Name': 'pitcher',
            'ERA': 'era',
            'FIP': 'fip',
            'HR/9': 'hr9',
            'K%': 'k_rate',
            'BB%': 'bb_rate'
        })

        features = ['pitcher', 'era', 'fip', 'hr9', 'k_rate', 'bb_rate']
        df = df[features]
        df.dropna(inplace=True)

        return df.reset_index(drop=True)

    except Exception as e:
        print("Error loading pitcher data:", e)
        return pd.DataFrame(columns=[
            'pitcher', 'era', 'fip', 'hr9', 'k_rate', 'bb_rate'
        ])
    except Exception as e:
        print("Error loading data:", e)
        traceback.print_exc()
        return pd.DataFrame(columns=[
            'player', 'slg', 'iso', 'hr_fb', 'bb_rate', 'k_rate', 'pa', 'hr'
        ])
