from utils.io import load_season

season1 = load_season("data/PL-season-2324.csv")
season2 = load_season("data/PL-season-2425.csv")

df = pd.concat([season1, season2], ignore_index=True)
