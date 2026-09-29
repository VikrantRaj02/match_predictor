import pandas as pd, glob

df = pd.concat([pd.read_csv(f) for f in glob.glob("data/*.csv")])
print(df.shape)
print(df[["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]].head())
print(df["FTR"].value_counts(normalize=True))