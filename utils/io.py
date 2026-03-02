import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    print(">>> USING CORRECT load_data() <<<")
    pl23_24 = pd.read_csv("data/PL-season-2324.csv")
    pl24_25 = pd.read_csv("data/PL-season-2425.csv")

    pl23_24["Season"] = "2023-24"
    pl24_25["Season"] = "2024-25"

    combined = pd.concat([pl23_24, pl24_25], ignore_index=True)

    home = combined.copy()
    home["team"] = home["HomeTeam"]
    home["opponent"] = home["AwayTeam"]
    home["is_home"] = True
    home["goals_for"] = home["FTHG"]
    home["goals_against"] = home["FTAG"]
    home["shots"] = home["HS"]
    home["shots_on_target"] = home["HST"]
    home["corners"] = home["HC"]
    home["fouls"] = home["HF"]
    home["yellow"] = home["HY"]
    home["red"] = home["HR"]
    home["points"] = ((home["FTR"] == "H") * 3 + (home["FTR"] == "D") * 1)

    home = home.drop(columns=[
        "HomeTeam","AwayTeam","Referee","FTHG","FTAG","HS","AS","HST","AST",
        "HC","AC","HF","AF","HY","AY","HR","AR"
    ])

    away = combined.copy()
    away["team"] = away["AwayTeam"]
    away["opponent"] = away["HomeTeam"]
    away["is_home"] = False
    away["goals_for"] = away["FTAG"]
    away["goals_against"] = away["FTHG"]
    away["shots"] = away["AS"]
    away["shots_on_target"] = away["AST"]
    away["corners"] = away["AC"]
    away["fouls"] = away["AF"]
    away["yellow"] = away["AY"]
    away["red"] = away["AR"]
    away["points"] = ((away["FTR"] == "A") * 3 + (away["FTR"] == "D") * 1)

    away = away.drop(columns=[
        "HomeTeam","AwayTeam","Referee","FTHG","FTAG","HS","AS","HST","AST",
        "HC","AC","HF","AF","HY","AY","HR","AR"
    ])

    team_matches = pd.concat([home, away], ignore_index=True)

    team_matches["Date"] = team_matches["Date"].astype(str).str.strip()
    team_matches["Date"] = team_matches["Date"].str.replace("-", "/", regex=False)

    team_matches["Date"] = pd.to_datetime(
        team_matches["Date"],
        format="%d/%m/%y",
        errors="coerce"
    )

    team_matches = team_matches.dropna(subset=["Date"])
    team_matches = team_matches.sort_values(["Season", "Date"])
    team_matches["matchweek"] = team_matches.groupby(["Season", "team"]).cumcount() + 1

    metrics = ["goals_for", "shots", "shots_on_target", "corners"]
    for m in metrics:
        team_matches[f"{m}_roll"] = (
            team_matches.groupby(["Season", "team"])[m]
            .rolling(window=3, min_periods=1).mean()
            .reset_index(level=[0,1], drop=True)
        )

    team_summary = (
        team_matches.groupby(["Season", "team"], as_index=False)
        .agg(
            total_points=("points","sum"),
            total_goals_for=("goals_for","sum"),
            total_goals_against=("goals_against","sum"),
            total_shots=("shots","sum"),
            total_shots_on_target=("shots_on_target","sum"),
            total_corners=("corners","sum"),
            total_fouls=("fouls","sum"),
            total_yellow=("yellow","sum"),
            total_red=("red","sum")
        )
    )

    team_summary["goal_difference"] = (
        team_summary["total_goals_for"] - team_summary["total_goals_against"]
    )

    team_summary = (
        team_summary.sort_values(["Season","total_points"], ascending=[True,False])
        .assign(
            league_position=lambda df: df.groupby("Season")["total_points"]
            .rank(method="first", ascending=False).astype(int)
        )
    )

    homeaway_summary = (
        team_matches.groupby(["Season","team","is_home"])
        .agg(
            total_points=("points","sum"),
            total_goals_for=("goals_for","sum"),
            total_goals_against=("goals_against","sum")
        )
        .reset_index()
    )

    return team_matches, team_summary, homeaway_summary
