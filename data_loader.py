import pandas as pd
from pybaseball import batting_stats, pitching_stats
import traceback

# =========================
# Load Batters
# =========================
def load_batter_features():
    try:
        print(">>> Loading batters...")
        df = batting_stats(2024, qual=20)
import numpy as np

# Simulate environmental context
df['park_factor'] = np.random.normal(loc=1.0, scale=0.1, size=len(df))          # around league average
df['wind'] = np.random.normal(loc=5, scale=3, size=len(df))                     # 5 mph avg
df['temperature'] = np.random.normal(loc=75, scale=10, size=len(df))            # degrees F
df['humidity'] = np.random.normal(loc=50, scale=15, size=len(df))               # percentage
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

        print(">>> Batters loaded:", len(df))
        return df.reset_index(drop=True)

    except Exception as e:
        print(">>> ERROR loading batter data:", e)
        traceback.print_exc()
        return pd.DataFrame(columns=[
            'player', 'slg', 'iso', 'hr_fb', 'bb_rate', 'k_rate', 'pa', 'hr'
        ])

# =========================
# Load Pitchers
# =========================
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
# 1. Rename pitcher stats to avoid conflict
df = df.rename(columns={
    'k_rate': 'k_rate_p',
    'bb_rate': 'bb_rate_p'
})

# 2. Define full list of features (including weather & park)
full_features = [
    'slg', 'iso', 'hr_fb', 'bb_rate', 'k_rate', 'pa',
    'era', 'fip', 'hr9', 'k_rate_p', 'bb_rate_p',
    'park_factor', 'wind', 'temperature', 'humidity'
]

# 3. Create binary target
df['target'] = (df['hr'] >= 1).astype(int)

# 4. Drop any rows missing required features
features = [f for f in full_features if f in df.columns]
df = df.dropna(subset=features + ['target'])

# 5. Train the model
X = df[features]
y = df['target']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_scaled, y)
        df = df[['pitcher', 'era', 'fip', 'hr9', 'k_rate', 'bb_rate']]
        df.dropna(inplace=True)

        print(">>> Pitchers loaded:", len(df))
        return df.reset_index(drop=True)

    except Exception as e:
        print(">>> ERROR loading pitcher data:", e)
        traceback.print_exc()
        return pd.DataFrame(columns=[
            'pitcher', 'era', 'fip', 'hr9', 'k_rate', 'bb_rate'
        ])
