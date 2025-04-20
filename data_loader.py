from pybaseball import batting_stats
import pandas as pd

def load_real_data():
    try:
        # Get season-to-date stats (change year if needed)
        df = batting_stats(2024, qual=20)

        # Select relevant columns
        df = df[['Name', 'HR', 'HR/FB', 'SLG', 'ISO', 'PA']]
        df = df.rename(columns={'Name': 'player'})

        # Fill any missing values
        df.fillna(0, inplace=True)

        # Map real stats to mock features (f0 to f9) for current model compatibility
        stat_cols = ['HR', 'HR/FB', 'SLG', 'ISO', 'PA']
        for i, col in enumerate(stat_cols):
            df[f'f{i}'] = pd.qcut(df[col], 10, labels=False, duplicates='drop')
        
        # Fill the remaining fake features (f5 to f9) with small adjustments
        for i in range(5, 10):
            df[f'f{i}'] = df[f'f{i - 5}'] + i * 0.1

        return df[['player'] + [f'f{i}' for i in range(10)]]

    except Exception as e:
        print("Error loading real data:", e)
        return pd.DataFrame(columns=['player'] + [f'f{i}' for i in range(10)])
