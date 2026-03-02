import streamlit as st
from utils.io import load_data
from charts.charts import chart_team_points, chart_goal_difference

st.title("Premier League: Two Seasons in Review")

team_matches, team_summary, homeaway_summary = load_data()


st.write("""By looking across points, goal difference, attacking rhythm, and home‑versus‑away performance, we can trace how each team’s 
story has unfolded over the last two Premier League seasons. I provide a brief overview of this in the story page, 
with more graphics and greater opportunity for interactivity on the explore page.""")


st.header("Who improved the most?")
st.altair_chart(chart_team_points(team_summary), width = 250)

st.header("Which teams dominated offensively?")
st.altair_chart(chart_goal_difference(team_summary))
