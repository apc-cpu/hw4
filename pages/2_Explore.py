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

st.header("How did teams perform across the two seasons?")
st.write("""This view compares total points across the 2023–24 and 2024–25 seasons. 
Some clubs show remarkable stability, while others swing dramatically from one 
season to the next.

Arsenal, for example, have been one of the most consistent performers across 
both seasons, maintaining high point totals and staying near the top of the table. 
In contrast, Chelsea experienced a much more uneven trajectory, with stronger 
runs mixed with periods of inconsistency that caused their league position to 
fluctuate more noticeably.""")

st.altair_chart(chart_team_points(team_summary))


st.header("Which teams controlled matches through goal difference?")
st.write("""Goal difference often reveals more about a team’s underlying strength than points alone. 
Teams with strong attacking output and solid defensive structure tend to separate 
themselves from the rest of the league.

Manchester City and Arsenal consistently post high goal differences, reflecting dominant performances at both ends of the pitch. Meanwhile, teams like 
Luton Town sit at the opposite end of the scale, struggling to keep matches competitive over the long season.""")

st.altair_chart(chart_goal_difference(team_summary))


st.header("How consistent was each team’s attacking output?")
st.write("""This rolling average chart smooths out match-to-match volatility and highlights longer-term trends. You can switch between metrics—goals, shots, shots on target, 
and corners—to see how a team’s attacking rhythm evolved over the season.

Arsenal again stand out for their steady attacking production, rarely dipping below their seasonal average. On the other hand, a team like Manchester United 
shows more pronounced peaks and dips, with strong attacking bursts followed by periods of stagnation.""")

st.altair_chart(chart_rolling(team_matches))


st.header("Does home advantage still matter?")
st.write("""Home advantage's impact varies widely across clubs.

Teams like Liverpool and Newcastle tend to be significantly stronger at home, earning a large share of their points at their own stadiums. Meanwhile, clubs such 
as Brighton or West Ham often travel surprisingly well, showing good form when playing away.""")

st.altair_chart(chart_homeaway(homeaway_summary))
