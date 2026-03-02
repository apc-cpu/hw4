import altair as alt

team_select = alt.selection_point(fields=["team"], name="TeamSelect", toggle=False)

season_param = alt.param(
    name="Season",
    bind=alt.binding_select(options=[]),
)

metric_param = alt.param(
    name="Metric",
    bind=alt.binding_select(options=[
        "goals_for_roll",
        "shots_roll",
        "shots_on_target_roll",
        "corners_roll"
    ]),
    value="goals_for_roll"
)

team_filter_param = alt.param(
    name="TeamFilter",
    bind=alt.binding_select(options=["All"]),
    value="All"
)

homeaway_brush = alt.selection_interval(
    name="HomeAwayBrush",
    encodings=["x", "y"]
)

team_filter_logic = (
    "(TeamFilter != 'All') ? datum.team == TeamFilter : "
    "(TeamSelect != null && TeamSelect.team != null) ? datum.team == TeamSelect.team : "
    "true"
)

def chart_team_points(team_summary):
    seasons = sorted(team_summary["Season"].unique())
    season_param.bind.options = seasons
    season_param.value = seasons[0]

    teams = sorted(team_summary["team"].unique())
    team_filter_param.bind.options = ["All"] + teams

    dot = (
        alt.Chart(team_summary)
        .mark_circle(size=200)
        .encode(
            x=alt.X("total_points:Q", title="Total Points"),
            y=alt.Y("team:N", sort="-x", title="Team"),
            color=alt.condition(team_select, "team:N", alt.value("lightgray")),
            tooltip=[
                "team:N",
                "Season:N",
                "total_points:Q",
                "goal_difference:Q",
                "league_position:Q"
            ]
        )
        .add_params(season_param, team_select, team_filter_param)
        .transform_filter("datum.Season == Season")
        .transform_filter(team_filter_logic)
        .properties(width=400, height=500, title="Team Performance by Season")
    )
    return dot

def chart_goal_difference(team_summary):
    seasons = sorted(team_summary["Season"].unique())
    season_param.bind.options = seasons
    season_param.value = seasons[0]

    teams = sorted(team_summary["team"].unique())
    team_filter_param.bind.options = ["All"] + teams

    bar = (
        alt.Chart(team_summary)
        .mark_bar()
        .encode(
            x=alt.X("goal_difference:Q", title="Goal Difference"),
            y=alt.Y("team:N", sort="-x"),
            color=alt.condition(team_select, "team:N", alt.value("lightgray")),
            tooltip=["team:N", "goal_difference:Q"]
        )
        .add_params(team_select, season_param, team_filter_param)
        .transform_filter("datum.Season == Season")
        .transform_filter(team_filter_logic)
        .properties(width=500, height=500, title="Goal Difference by Team")
    )
    return bar

def chart_rolling(team_matches):
    seasons = sorted(team_matches["Season"].unique())
    season_param.bind.options = seasons
    season_param.value = seasons[0]

    teams = sorted(team_matches["team"].unique())
    team_filter_param.bind.options = ["All"] + teams

    rolling_chart = (
        alt.Chart(team_matches)
        .add_params(team_select, season_param, metric_param, team_filter_param)
        .transform_filter("datum.Season == Season")
        .transform_filter(team_filter_logic)
        .transform_calculate(metric_value=f"datum[{metric_param.name}]")
        .mark_line()
        .encode(
            x=alt.X("matchweek:Q", title="Matchweek"),
            y=alt.Y("metric_value:Q", title="Rolling Average"),
            color=alt.Color("team:N"),
            tooltip=[
                "team:N",
                "Season:N",
                "matchweek:Q",
                alt.Tooltip("metric_value:Q", title="Rolling Avg")
            ]
        )
        .properties(width=800, height=400, title="Rolling Attacking Performance Over Time")
    )
    return rolling_chart

def chart_homeaway(homeaway_summary):
    seasons = sorted(homeaway_summary["Season"].unique())
    season_param.bind.options = seasons
    season_param.value = seasons[0]

    teams = sorted(homeaway_summary["team"].unique())
    team_filter_param.bind.options = ["All"] + teams

    homeaway_chart = (
        alt.Chart(homeaway_summary)
        .add_params(team_select, team_filter_param, season_param, homeaway_brush)
        .transform_filter("datum.Season == Season")
        .transform_filter(team_filter_logic)
        .mark_bar()
        .encode(
            x=alt.X("team:N", title="Team"),
            y=alt.Y("total_points:Q", title="Total Points"),
            color=alt.Color("is_home:N", title="Home/Away"),
            opacity=alt.condition(homeaway_brush, alt.value(1), alt.value(0.3)),
            tooltip=["team:N", "Season:N", "is_home:N", "total_points:Q"]
        )
        .properties(width=700, height=400, title="Home vs Away Performance")
    )
    return homeaway_chart
