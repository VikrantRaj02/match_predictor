# Premier League Match Predictor
A machine learning model that predicts the match results (home win/draw/away win) for the Premier League (Football) using Elo team ratings and logistic regression.

When the model is unable to see 2025-26 season, it predicts the results accurately 50% of the time, compared with 42.6% for always picking the home team and Bet365's 48.9% result prediction accuracy.

**Try it live:** https://matchpredictor-momakvqja2rc8bgoyz6ybd.streamlit.app/

## Results

### Test accuracy by version (2025-26 season, 380 matches)

| Version | Accuracy |
| --- | --- |
| Always pick home win (Baseline) | 42.6% |
| Recent form features | 46.8% |
| Recent form + Elo ratings | 48.2% |
| Recent form + Elo, with feature scaling | 48.9% |
| Elo ratings only | 48.4% |
| **Elo ratings only, tuned (K=40)** | **50.0%** |

With 380 test matches, one match is worth around 0.26 percentage points, so small differences between versions may be due to chance.

### Comparison with a bookmaker (2025-26)
|| **Accuracy** | **Log Loss** |
|---|---|---|
| Always pick home win | 42.6% | -- |
| This model | 50.0% | 1.041 |
| Bet365 | 48.9% | 1.0185 |

The bookmaker figures are from the Bet365 pre-match odds in the dataset. I use the outcome with the lowest odds, and probabilities were calculated as 1/odds, rescaled to sum to 1.

in 25-26 season, the model's accuracy was comparable to Bet365's, while the Bet365's probabilities scored better on log loss. It was a single season so it doesn't tell the actual comparison of the two models.

### Confusion Matrix

| **Recent form only** | **Form + Elo (K = 20)** | **Final: Elo only (K = 40)** |
|---|---|---|
| ![Form-only](images/1st%20output%20(178%20correct).png) | ![Form + Elo (K = 20)](images/2nd%20output%20(183%20correct).png) | ![Elo only (K = 40)](images/3rd%20output%20(190%20correct).png) |


|| **Recent form only** | **Form + Elo (K = 20)** | **Final: Elo only (K = 40)** |
|---|---|---|---|
| Home wins correct (of 162) | 129 | 124 | 127 |
| Away wins correct (of 114) | 49 | 59 | 63 |
| Draws correct (of 104) | 0 | 0 | 0 |
| Total correct (of 380) | 178 | 183 | 190 |

Elo increases the number of correct away-win predictions from 49 to 59, conversely it decreases the number of correct home-win predictions from 129 to 124. The tuning of the Elo only model improved the accuracy compared to the K = 20 version.

None of the versions predicted a draw for any match: in every 2025-26 match, any sort of win had a higher predicted probability than a draw.

## How it works

**Data:** Premier League results from [football-data.co.uk](https://www.football-data.co.uk) from 2016-17 to 2025-26, plus the 2026-27 season so far for live predictions.

**Elo Ratings:** Every team starts at 1500 Elo. The two ratings (+60 for home team) give the expected result. When the match ends, the formula used for Elo adjustment is K × (actual result - expected result), with K = 40. Each match uses the ratings from before the kick-off, so the model doesn't see the result it's predicting.

**Model:** Logistic Regression, with standardised inputs, takes the home and away Elo ratings and outputs a probability for home win, draw, and away win. The pick is the outcome with the highest probability.

**Training & Testing:** The training was first done on matches till 2024-25 and the testing done on 2025-26. Later, the training was done on matches till 2023-24 season and testing on 2024-25. A few of the early matches were excluded since they didn't have enough previous games to calculate the form features used in experiments.

**Decision Making:** Elo, feature scaling and random forest were judged on their accuracy on the test season. This was done with 25-26 as the test season. The choice of features, elo tuning and draw rule were done with 24-25 as its test season. Log loss was used for the features and elo rating while draw rule was done with accuracy.

## What didn't work

Everything here was done on the 2024-25 validation season.

**Form Features:** average goals scored, goals conceded, shots, shots on target and points over their previous 5 and 10 matches. Elo was at K = 20.
Results:

| **Features** | **Accuracy** | **Log Loss** |
|---|---|---|
| Elo + 5-game form | 52.7% | 0.9939 |
| Elo + 5-game form + shots on target | 52.4% | 0.9940 |
| Elo + 10-game form | 51.1% | 1.0027 |
| Elo + 5- and 10-game form | 51.4% | 1.0101 |
| Elo only | 53.2% | 0.9930 |

Since none of the form features didn't do anything to improve the model more than Elo alone. This is why the final model uses Elo only. A possible reason would be Elo already accounts for the other features to an extent.

**Elo Settings:** K values were tested from 10 to 80 and home advantage values from 40 to 100.

- K = 40 gave the lowest log loss (0.9857), compared with the initial 0.9930 at K = 20. Log loss rose again at higher values (0.9936 at K = 80).
- Home advantage values between 40 and 100 changed by 0.0022 or less at each K value. This might be because the model learns the home advantage from the data but that wasn't directly tested.
- Using a season resetter or pulling ratings towards 1500 at the start of each new season made the log loss worse at every level (0.9860-0.9879 vs 0.9857 without).
- Adjusting rating changes based on how many more goals a team scored than its opposition also worsened the log loss (0.9898 vs 0.9857).

**Draw Rule:** The model never predicts draws. This made me test a draw rule where it predicts draws when the home and away wins were within a set margin of probability. With no rule, the accuracy was 53.8% while with margins 0.05, 0.10, 0.15 and 0.20 it was 51.9%, 52.2%, 49.5% and 48.1% respectively. I rejected the rule.

**Random Forest:** This scored less than the logistic regression on the test season in every version compared: 45.3% vs 46.8% (form features), 47.9% vs 48.2% (Elo), 48.2% vs 50.0% (Elo after tuning).

## Live Predictions

**Gameweek 6:** 5 of 10 correct (50%)
| **Matchup** | **Predicted** | **Actual** |
|---|---|---|
| Arsenal vs Leeds | Arsenal | Arsenal |
| Aston Villa vs Brentford | Aston Villa | Draw |
| Ipswich vs Fulham | Fulham | Ipswich |
| Chelsea vs Bournemouth | Chelsea | Chelsea |
| Sunderland vs Brighton | Brighton | Brighton |
| Man United vs Tottenham | Man United | Draw |
| Crystal Palace vs Nott'm Forest | Crystal Palace |
| Hull vs Everton | Everton | Draw |
| Liverpool vs Man City | Man City | Man City |
| Coventry vs Newcastle | Newcastle | Coventry |

## How to Run

1. Install Libraries
```
pip install pandas scikit-learn matplotlib requests
```
2. Download Data
```
python download.py
```
3. Open model.ipynb and run all cells

**Edit the fixtures list in the last cell using the names in the data to get live predictions.**

## Possible Next Steps

- Comparing with the bookmaker over several seasons.
- Validate settings across several seasons.
- Download earlier season data to feed the Elo in the training period better.
- Testing lower starting rating for newly promoted teams.
- Build an app to pick two teams and see prediction.

## Tools

Python, pandas, scikit-learn, matplotlib, requests

## Data

Match data and betting odds from football-data.co.uk 