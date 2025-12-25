import pandas as pd

TRAIN_FILE = "data/training.csv"
SUGGEST_FILE = "data/suggestions.csv"

df_train = pd.read_csv(TRAIN_FILE)
df_suggest = pd.read_csv(SUGGEST_FILE)

df_final = pd.concat([df_train, df_suggest], ignore_index=True)

df_final.to_csv(TRAIN_FILE, index=False, quoting=1)

print(f"✅ Training bertambah {len(df_suggest)} data")
