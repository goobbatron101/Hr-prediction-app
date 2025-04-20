import pandas as pd
import numpy as np
import traceback
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
