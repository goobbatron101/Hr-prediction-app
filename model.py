import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from data_loader import load_batter_features

# Load real batter data
df = load_batter_features()
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from data_loader import load_batter_features, load_pitcher_features

# Load data
batters = load_batter_features()
pitchers = load_pitcher_features()

# Randomly assign a pitcher to each batter
np.random.seed(42)
pitcher_sample = pitchers.sample(n=len(batters), replace=True).reset_index(drop=True)

# Merge hitter and pitcher stats
df = pd.concat([batters.reset_index(drop=True), pitcher_sample], axis=1)

# Create binary target
df['target'] = (df['hr'] >= 1).astype(int)

# Select features
features = [
    'slg', 'iso', 'hr_fb', 'bb_rate', 'k_rate', 'pa',    # Hitter
    'era', 'fip', 'hr9', 'k_rate_p', 'bb_rate_p'          # Pitcher (renamed below)
]

# Rename pitcher columns to avoid overlap with hitter columns
df = df.rename(columns={
    'k_rate': 'k_rate_p',
    'bb_rate': 'bb_rate_p'
})

# Drop rows with missing values
df = df.dropna(subset=features + ['target'])

# Scale features
X = df[features]
y = df['target']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_scaled, y)

# Prediction function
def predict_home_runs(df_input):
    # Sample pitchers again for prediction (mock matchups)
    pitcher_input = pitchers.sample(n=len(df_input), replace=True).reset_index(drop=True)
    df_input = df_input.reset_index(drop=True)
    df_combined = pd.concat([df_input, pitcher_input], axis=1)

    df_combined = df_combined.rename(columns={
        'k_rate': 'k_rate_p',
        'bb_rate': 'bb_rate_p'
    })

    X_pred = df_combined[features]
    X_scaled_pred = scaler.transform(X_pred)
    probs = model.predict_proba(X_scaled_pred)[:, 1]

    df_combined['HR_Probability'] = probs
    df_combined['Recommendation'] = pd.cut(
        probs,
        bins=[0, 0.2, 0.35, 1.0],
        labels=["Fade", "Watchlist", "Positive EV Bet"]
    )

    return df_combined[['player', 'pitcher', 'HR_Probability', 'Recommendation']].sort_values(
        by='HR_Probability', ascending=False
    )
# Define features and binary target (1 if HR ≥ 1, else 0)
df['target'] = (df['hr'] >= 1).astype(int)
X = df[['slg', 'iso', 'hr_fb', 'bb_rate', 'k_rate', 'pa']]
y = df['target']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train logistic regression
model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_scaled, y)

# Prediction function
def predict_home_runs(input_df):
    X_input = input_df[['slg', 'iso', 'hr_fb', 'bb_rate', 'k_rate', 'pa']]
    X_scaled_input = scaler.transform(X_input)
    probs = model.predict_proba(X_scaled_input)[:, 1]

    result_df = input_df.copy()
    result_df['HR_Probability'] = probs
    result_df['Recommendation'] = pd.cut(
        probs,
        bins=[0, 0.2, 0.35, 1.0],
        labels=["Fade", "Watchlist", "Positive EV Bet"]
    )
    return result_df.sort_values(by='HR_Probability', ascending=False)
