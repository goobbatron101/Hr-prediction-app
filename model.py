import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from data_loader import load_batter_features, load_pitcher_features

# Load data
batters = load_batter_features()
pitchers = load_pitcher_features()

# Randomly assign pitchers to batters
np.random.seed(42)
pitcher_sample = pitchers.sample(n=len(batters), replace=True).reset_index(drop=True)
df = pd.concat([batters.reset_index(drop=True), pitcher_sample], axis=1)

# Rename pitcher stats to avoid name collisions
df = df.rename(columns={
    'k_rate': 'k_rate_p',
    'bb_rate': 'bb_rate_p'
})

# Target: 1 if HR ≥ 1
df['target'] = (df['hr'] >= 1).astype(int)

# Rename pitcher stats
df = df.rename(columns={
    'k_rate': 'k_rate_p',
    'bb_rate': 'bb_rate_p'
})

# Full intended feature list
full_features = [
    'slg', 'iso', 'hr_fb', 'bb_rate', 'k_rate', 'pa',
    'era', 'fip', 'hr9', 'k_rate_p', 'bb_rate_p'
]

# Use only features that exist in the actual DataFrame
features = [f for f in full_features if f in df.columns]
df = df.dropna(subset=features + ['target'])

# Train model
X = df[features]
y = df['target']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_scaled, y)

def predict_home_runs(df_input):
    import numpy as np

    # Simulate weather & park if not present
    if 'park_factor' not in df_input.columns:
        df_input['park_factor'] = np.random.normal(1.0, 0.1, len(df_input))
        df_input['wind'] = np.random.normal(5, 3, len(df_input))
        df_input['temperature'] = np.random.normal(75, 10, len(df_input))
        df_input['humidity'] = np.random.normal(50, 15, len(df_input))

    # Assign random pitchers
    pitcher_input = pitchers.sample(n=len(df_input), replace=True).reset_index(drop=True)
    df_input = df_input.reset_index(drop=True)
    df_combined = pd.concat([df_input, pitcher_input], axis=1)

    # Rename pitcher stats
    df_combined = df_combined.rename(columns={
        'k_rate': 'k_rate_p',
        'bb_rate': 'bb_rate_p'
    })

    # Make predictions
    X_pred = df_combined[features]
    X_scaled_pred = scaler.transform(X_pred)
    probs = model.predict_proba(X_scaled_pred)[:, 1]

    # Add results
    df_combined['HR_Probability'] = probs
    df_combined['Recommendation'] = pd.cut(
        probs,
        bins=[0, 0.2, 0.35, 1.0],
        labels=["Fade", "Watchlist", "Positive EV Bet"]
    )

    # Return all relevant columns
    return df_combined[[
        'player', 'pitcher', 'HR_Probability', 'Recommendation',
        'park_factor', 'wind', 'temperature', 'humidity'
    ]].sort_values(by='HR_Probability', ascending=False)