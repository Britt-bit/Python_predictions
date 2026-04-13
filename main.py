from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.figsize"] = (8, 4.5)

DATA_PATH = Path(__file__).resolve().parent / "data" / "heart.csv"
df = pd.read_csv(DATA_PATH)
print(df.head())