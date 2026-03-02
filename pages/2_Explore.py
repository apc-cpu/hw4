import streamlit as st
from utils.io import load_data
from charts.charts import (
    chart_team_points,
    chart_goal_difference,
    chart_rolling,
    chart_homeaway
)

st.title("Explore the Premier League Data")

team_matches, team_summary, homeaway_summary = load_data()

st.subheader("Team Performance by Season")
st.altair_chart(chart_team_points(team_summary), use_container_width=True)

st.subheader("Goal Difference by Team")
st.altair_chart(chart_goal_difference(team_summary), use_container_width=True)

st.subheader("Rolling Attacking Performance")
st.altair_chart(chart_rolling(team_matches), use_container_width=True)

st.subheader("Home vs Away Performance")
st.altair_chart(chart_homeaway(homeaway_summary), use_container_width=True)
