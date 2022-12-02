import dash_bootstrap_components as dbc
import dash
import pandas as pd
import plotly.express as px

from dash import Dash, html, dcc, Input, Output, callback


dash.register_page(__name__, path="/")




@callback(
    Output("test", "children"),
    Input("start-station-picker", "value")
)
def test(start_station):
    return str(start_station)


@callback(
    Output("home-graph", "figure"),
    Input("start-station-picker", "value"),
    Input("end-station-picker", "value")
)
def choose_start_end_station(start_station, end_station):
    df = pd.read_csv("201811-citibike-tripdata.csv")
    data = (
        df
        .loc[df["start station id"] == start_station, :]
        .loc[df["end station id"] == end_station, :]
        .groupby("gender")
        ["tripduration"]
        .mean()
        .reset_index()
    )
    print(data.shape)
    print("YEs")

    return px.bar(data, x="gender", y="tripduration")


def layout():
    _layout = html.Div(
        [
            html.H1("This is home page"),
            dbc.Row(
                [
                    dbc.Input(
                        id="start-station-picker", placeholder="Start station", type="number",
                    ),
                    dbc.Input(
                        id="end-station-picker", placeholder="End station", type="number"
                    )
                ]
            ),
            dbc.Row(dcc.Graph(id="home-graph")),
            dbc.Row(html.P(id="test"))
        ]
    )
    return _layout
