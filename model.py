import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Mock training (real model should be loaded or trained on real data)
def train_mock_model():
    np.random.seed(42)
    X = pd.DataFrame(np.random.normal(0, 1, (500, 10)), columns=[f'f{i}' for i in range(10)])
    y = np.random.choice([0, 1], size=500, p=[0.9, 0.1])
    model = LogisticRegression(class_weight='balanced', max_iter=1000)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model.fit(X_scaled, y)
    return model, scaler

model, scaler = train_mock_model()

def predict_home_runs(df):
    X = df.drop(columns=['player'])
    X_scaled = scaler.transform(X)
    probs = model.predict_proba(X_scaled)[:, 1]
    df['HR_Probability'] = probs
    df['Recommendation'] = pd.cut(probs, bins=[0, 0.2, 0.35, 1], labels=["Fade", "Watchlist", "Positive EV Bet"])
    return df.sort_values(by='HR_Probability', ascending=False)
