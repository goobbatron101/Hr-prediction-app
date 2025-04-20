from pybaseball import batting_stats
import pandas as pd

def load_real_data():
    # Pull full-season MLB hitter stats
    df = batting_stats(2024, qual=20)

    # Select key features and rename to match the model placeholder structure
    df = df[['Name', 'HR', 'HR/FB', 'SLG', 'ISO', 'PA']]
    df = df.rename(columns={'Name': 'player'})

    # Create 10 fake model features (f0 to f9) using real data as input
    for i in range(10):
        df[f'f{i}'] = pd.qcut(df['HR'], 10, labels=False, duplicates='drop') + (i * 0.1)

    return df[['player'] + [f'f{i}' for i in range(10)]]
