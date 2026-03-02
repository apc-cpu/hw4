import streamlit as st
from utils.io import load_data
from charts.charts import chart_team_points, chart_goal_difference, chart_season_average_points

st.title("Premier League: Two Seasons in Review")

team_matches, team_summary, homeaway_summary = load_data()


st.subheader("Quick context")
st.caption("A small static summary chart comparing overall average points by season.")
st.altair_chart(chart_season_average_points(team_summary), width="content")

