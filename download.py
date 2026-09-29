import requests, os

os.makedirs("data", exist_ok=True)
for start in range(16, 26):
    code = f"{start}{start+1}"
    url = f"https://www.football-data.co.uk/mmz4281/{code}/E0.csv"
    r = requests.get(url)
    with open(f"data/20{code[:2]}-{code[2:]}.csv", "wb") as f:
        f.write(r.content)
    print("Downloaded", code)