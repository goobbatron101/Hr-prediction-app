import pandas as pd
import numpy as np

def load_mock_data():
    n = 30  # number of players
    df = pd.DataFrame({
        'player': [f'Player {i}' for i in range(n)],
        'f0': np.random.normal(0, 1, n),
        'f1': np.random.normal(0, 1, n),
        'f2': np.random.normal(0, 1, n),
        'f3': np.random.normal(0, 1, n),
        'f4': np.random.normal(0, 1, n),
        'f5': np.random.normal(0, 1, n),
        'f6': np.random.normal(0, 1, n),
        'f7': np.random.normal(0, 1, n),
        'f8': np.random.normal(0, 1, n),
        'f9': np.random.normal(0, 1, n),
    })
    return df
