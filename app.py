import glob
import pandas as pd
import streamlit as st
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

st.title("Premier League Match Predictor")
st.write("Predicts match results using Elo ratings and logistic regression.")

def elo_expected(r_home, r_away, home_adv=60):
    return 1 / (1 + 10 ** ((r_away - (r_home + home_adv)) / 400))

def compute_elo(data, K=40, home_adv=60):
    ratings, home_elo, away_elo = {}, [], []
    for _, row in data.iterrows():
        h, a = row["HomeTeam"], row["AwayTeam"]
        rh, ra = ratings.get(h,1500), ratings.get(a,1500)
        home_elo.append(rh)
        away_elo.append(ra)
        actual = {"H": 1, "D": 0.5, "A": 0}[row["FTR"]]
        change = K * (actual - elo_expected(rh, ra, home_adv))
        ratings[h], ratings[a] = rh + change, ra -change
    return home_elo, away_elo, ratings

@st.cache_resource
def load_model():
    df = pd.concat([pd.read_csv(f, encoding="latin-1", on_bad_lines="skip") for f in glob.glob("data/*.csv")])
    df = df.dropna(subset=["FTR"])
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, format="mixed")
    df = df.sort_values("Date").reset_index(drop=True)
    df["home_elo"], df["away_elo"], ratings = compute_elo(df)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    model.fit(df[["home_elo", "away_elo"]], df["FTR"])
    return df, ratings, model

df, ratings, model = load_model()

latest = df["Date"].max()
season_start = pd.Timestamp(latest.year if latest.month >= 8 else latest.year - 1, 8, 1)
current_teams = sorted(set(df.loc[df["Date"] >= season_start, "HomeTeam"]))

st.header("Predict a match")
col1, col2 = st.columns(2)
home = col1.selectbox("Home Team", current_teams)
away = col2.selectbox("Away Team", current_teams, index=1)

if home == away:
    st.warning("Pick two different teams.")
else:
    X = pd.DataFrame([{"home_elo": ratings[home], "away_elo": ratings[away]}])
    p = dict(zip(model.classes_, model.predict_proba(X)[0]))

    c1, c2, c3 = st.columns(3)
    c1.metric(f"{home} win", f"{p['H']:.0%}")
    c2.metric("Draw", f"{p['D']:.0%}")
    c3.metric(f"{away} win", f"{p['A']:.0%}")

    labels = {"H": f"{home} win", "D": "Draw", "A": f"{away} win"}
    pick = max(p, key=p.get)
    st.subheader(f"Prediction: {labels[pick]}")
    st.caption(f"Current Elo ratings: {home} {ratings[home]:.0f}, {away} {ratings[away]:.0f}")


st.header("Current Elo ratings")
table = pd.DataFrame({"Team": current_teams, "Elo": [round(ratings[t]) for t in current_teams]})
table = table.sort_values("Elo", ascending=False).reset_index(drop=True)
table.index += 1
st.dataframe(table, use_container_width=True)