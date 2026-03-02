import streamlit as st
from utils.io import load_data
from charts.charts import chart_team_points, chart_goal_difference

st.title("Premier League: Two Seasons in Review")

team_matches, team_summary, homeaway_summary = load_data()

st.header("Who improved the most?")
st.write("Narrative text here…")
st.altair_chart(chart_team_points(team_summary), use_container_width=True)

st.header("Which teams dominated offensively?")
st.write("Narrative text here…")
st.altair_chart(chart_goal_difference(team_summary), use_container_width=True)
