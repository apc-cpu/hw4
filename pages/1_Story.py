import streamlit as st
from utils.io import load_data
from charts.charts import chart_team_points, chart_goal_difference, chart_season_average_points

st.title("Premier League: Two Seasons in Review")

team_matches, team_summary, homeaway_summary = load_data()


st.write("""By looking across points, goal difference, attacking rhythm, and home‑versus‑away performance, we can trace how each team’s 
story has unfolded over the last two Premier League seasons. I provide a brief overview of this in the story page, 
with more graphics and greater opportunity for interactivity on the explore page.""")



st.subheader("Quick context")
st.caption("A small static summary chart comparing overall average points by season.")
st.altair_chart(chart_season_average_points(team_summary), width="content")

