import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from data_loader import load_batter_features

# Load real batter data
df = load_batter_features()

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
