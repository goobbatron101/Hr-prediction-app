from pybaseball import batting_stats
import pandas as pd

def load_batter_features():
    try:
        # Pull 2024 season batter stats
        df = batting_stats(2024, qual=20)

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

    except Exception as e:
        print("Error loading data:", e)
        return pd.DataFrame(columns=[
            'player', 'slg', 'iso', 'hr_fb', 'bb_rate', 'k_rate', 'pa', 'hr'
        ])
