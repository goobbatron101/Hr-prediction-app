import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from data_loader import load_batter_features, load_pitcher_features

# Load data
batters = load_batter_features()
pitchers = load_pitcher_features()

# Match batters to pitchers
np.random.seed(42)
pitcher_sample = pitchers.sample(n=len(batters), replace=True).reset_index(drop=True)
df = pd.concat([batters.reset_index(drop=True), pitcher_sample], axis=1)

# Rename pitcher columns
df = df.rename(columns={
    'k_rate': 'k_rate_p',
    'bb_rate': 'bb_rate_p'
})

# Simulate binary target: HR ≥ 1
df['target'] = (df['hr'] >= 1).astype(int)

# Features to use
full_features = [
    'slg', 'iso', 'hr_fb', 'bb_rate', 'k_rate', 'pa',
    'era', 'fip', 'hr9', 'k_rate_p', 'bb_rate_p',
    'park_factor', 'wind', 'temperature', 'humidity'
]
features = [f for f in full_features if f in df.columns]
df = df.dropna(subset=features + ['target'])

# Scale features
scaler = StandardScaler()
X = scaler.fit_transform(df[features])
y = df['target']

# Train XGBoost model
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X, y)

# Predict function
def predict_home_runs(df_input):
    import numpy as np

    # Ensure park + weather features
    df_input = df_input.copy()
    df_input['park_factor'] = np.random.normal(1.0, 0.1, len(df_input))
    df_input['wind'] = np.random.normal(5, 3, len(df_input))
    df_input['temperature'] = np.random.normal(75, 10, len(df_input))
    df_input['humidity'] = np.random.normal(50, 15, len(df_input))

from data_loader import get_today_matchups

# Get real matchups
matchups = get_today_matchups()

if matchups.empty:
    print(">>> No matchups loaded, using fallback predictions.")
    return pd.DataFrame(columns=['player', 'pitcher', 'HR_Probability', 'Recommendation'])

# Merge matchup and pitcher data
df_combined = pd.merge(df_input, matchups, on='player', how='inner')
df_combined = pd.merge(df_combined, pitchers, on='pitcher', how='left')

# Merge real pitcher names into batter data
df_combined = pd.merge(df_input, matchups, on='player', how='inner')

# Merge in pitcher stats
df_combined = pd.merge(df_combined, pitchers, on='pitcher', how='left')

    # Rename pitcher stats
    df_combined = df_combined.rename(columns={
        'k_rate': 'k_rate_p',
        'bb_rate': 'bb_rate_p'
    })

    # Predict
    X_pred = scaler.transform(df_combined[features])
    probs = model.predict_proba(X_pred)[:, 1]

    df_combined['HR_Probability'] = probs
    df_combined['Recommendation'] = pd.cut(
        probs, bins=[0, 0.2, 0.35, 1.0],
        labels=["Fade", "Watchlist", "Positive EV Bet"]
    )

    return df_combined[
        ['player', 'pitcher', 'HR_Probability', 'Recommendation',
         'park_factor', 'wind', 'temperature', 'humidity']
    ].sort_values(by='HR_Probability', ascending=False)
