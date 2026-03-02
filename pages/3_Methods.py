import streamlit as st

st.title("Methods")

st.header("Data Source")
st.write("""This project uses Premier League data from the 2023–24 and 2024–25 seasons. The data comes from two CSV files that contain full and half time 
scores, shots, cards, corners, and other match statistics for every fixture in each season.""")

st.header("Data Preparation")
st.write("""To make the analysis consistent across seasons, the two CSV files were combined into a single dataset with a new Season column added to distinguish them.
Each match was then split into two team-level rows: one for the home team and one for the away team. This allowed us to compute team-level metrics such as 
goals for, goals against, shots, fouls, and points earned.""")

st.header("Summary Tables")
st.write("""From the cleaned match-level dataset, two summary tables were created:

- team_summary: total points, goals, shots, cards, and league position  
- homeaway_summary: home vs away performance for each team  

These tables power the visualizations in the Story and Explore pages.""")
