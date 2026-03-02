import altair as alt

def chart_team_points(team_summary):
    seasons = sorted(team_summary["Season"].unique())
    teams = sorted(team_summary["team"].unique())

    Season_TP = alt.param(
        name="Season_TP",
        bind=alt.binding_select(options=seasons),
        value=seasons[0]
    )

    TeamSelect_TP = alt.param(
        name="TeamSelect_TP",
        select=alt.SelectionPoint(fields=["team"], toggle=False)
    )

    TeamFilter_TP = alt.param(
        name="TeamFilter_TP",
        bind=alt.binding_select(options=["All"] + teams),
        value="All"
    )

    logic = (
        "(TeamFilter_TP != 'All') ? datum.team == TeamFilter_TP : "
        "(TeamSelect_TP != null && TeamSelect_TP.team != null) ? datum.team == TeamSelect_TP.team : "
        "true"
    )

    chart = (
        alt.Chart(team_summary)
        .add_params(Season_TP, TeamSelect_TP, TeamFilter_TP)
        .transform_filter("datum.Season == Season_TP")
        .transform_filter(logic)
        .mark_circle(size=200)
        .encode(
            x=alt.X("total_points:Q", title="Total Points"),
            y=alt.Y("team:N", sort="-x", title="Team"),
            color=alt.condition(TeamSelect_TP, "team:N", alt.value("lightgray")),
            tooltip=[
                "team:N",
                "Season:N",
                "total_points:Q",
                "goal_difference:Q",
                "league_position:Q"
            ]
        )
        .properties(width=450, height=500, title="Team Performance by Season")
    )

    return chart


def chart_goal_difference(team_summary):
    seasons = sorted(team_summary["Season"].unique())
    teams = sorted(team_summary["team"].unique())

    Season_GD = alt.param(
        name="Season_GD",
        bind=alt.binding_select(options=seasons),
        value=seasons[0]
    )

    TeamSelect_GD = alt.param(
        name="TeamSelect_GD",
        select=alt.SelectionPoint(fields=["team"], toggle=False)
    )

    TeamFilter_GD = alt.param(
        name="TeamFilter_GD",
        bind=alt.binding_select(options=["All"] + teams),
        value="All"
    )

    logic = (
        "(TeamFilter_GD != 'All') ? datum.team == TeamFilter_GD : "
        "(TeamSelect_GD != null && TeamSelect_GD.team != null) ? datum.team == TeamSelect_GD.team : "
        "true"
    )

    chart = (
        alt.Chart(team_summary)
        .add_params(Season_GD, TeamSelect_GD, TeamFilter_GD)
        .transform_filter("datum.Season == Season_GD")
        .transform_filter(logic)
        .mark_bar()
        .encode(
            x=alt.X("goal_difference:Q", title="Goal Difference"),
            y=alt.Y("team:N", sort="-x"),
            color=alt.condition(TeamSelect_GD, "team:N", alt.value("lightgray")),
            tooltip=["team:N", "goal_difference:Q"]
        )
        .properties(width=500, height=500, title="Goal Difference by Team")
    )

    return chart


def chart_rolling(team_matches):
    seasons = sorted(team_matches["Season"].unique())
    teams = sorted(team_matches["team"].unique())

    Season_ROLL = alt.param(
        name="Season_ROLL",
        bind=alt.binding_select(options=seasons),
        value=seasons[0]
    )

    Metric_ROLL = alt.param(
        name="Metric_ROLL",
        bind=alt.binding_select(options=[
            "goals_for_roll",
            "shots_roll",
            "shots_on_target_roll",
            "corners_roll"
        ]),
        value="goals_for_roll"
    )

    TeamSelect_ROLL = alt.param(
        name="TeamSelect_ROLL",
        select=alt.SelectionPoint(fields=["team"], toggle=False)
    )

    TeamFilter_ROLL = alt.param(
        name="TeamFilter_ROLL",
        bind=alt.binding_select(options=["All"] + teams),
        value="All"
    )

    logic = (
        "(TeamFilter_ROLL != 'All') ? datum.team == TeamFilter_ROLL : "
        "(TeamSelect_ROLL != null && TeamSelect_ROLL.team != null) ? datum.team == TeamSelect_ROLL.team : "
        "true"
    )

    chart = (
        alt.Chart(team_matches)
        .add_params(Season_ROLL, Metric_ROLL, TeamSelect_ROLL, TeamFilter_ROLL)
        .transform_filter("datum.Season == Season_ROLL")
        .transform_filter(logic)
        .transform_calculate(metric_value=f"datum[{Metric_ROLL.name}]")
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

    return chart


def chart_homeaway(homeaway_summary):
    seasons = sorted(homeaway_summary["Season"].unique())
    teams = sorted(homeaway_summary["team"].unique())

    Season_HA = alt.param(
        name="Season_HA",
        bind=alt.binding_select(options=seasons),
        value=seasons[0]
    )

    TeamSelect_HA = alt.param(
        name="TeamSelect_HA",
        select=alt.SelectionPoint(fields=["team"], toggle=False)
    )

    TeamFilter_HA = alt.param(
        name="TeamFilter_HA",
        bind=alt.binding_select(options=["All"] + teams),
        value="All"
    )

    Brush_HA = alt.param(
        name="Brush_HA",
        select=alt.SelectionInterval(encodings=["x", "y"])
    )

    logic = (
        "(TeamFilter_HA != 'All') ? datum.team == TeamFilter_HA : "
        "(TeamSelect_HA != null && TeamSelect_HA.team != null) ? datum.team == TeamSelect_HA.team : "
        "true"
    )

    chart = (
        alt.Chart(homeaway_summary)
        .add_params(Season_HA, TeamSelect_HA, TeamFilter_HA, Brush_HA)
        .transform_filter("datum.Season == Season_HA")
        .transform_filter(logic)
        .mark_bar()
        .encode(
            x=alt.X("team:N", title="Team"),
            y=alt.Y("total_points:Q", title="Total Points"),
            color=alt.Color("is_home:N", title="Home/Away"),
            opacity=alt.condition(Brush_HA, alt.value(1), alt.value(0.3)),
            tooltip=["team:N", "Season:N", "is_home:N", "total_points:Q"]
        )
        .properties(width=700, height=400, title="Home vs Away Performance")
    )

    return chart
