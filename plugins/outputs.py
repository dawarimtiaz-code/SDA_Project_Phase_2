from typing import Dict
import dash
from dash import dcc, html
import plotly.express as px

class DashboardWriter:
    def write(self, records: Dict) -> None:
        app = dash.Dash(_name_)

        tabs = dcc.Tabs([
            dcc.Tab(label='Top 10', children=[
                dcc.Graph(figure=px.bar(records["Top 10"], x="Country", y="GDP",
                                        title="Top 10 Countries by GDP",
                                        color="GDP", color_continuous_scale="Blues"))
            ]),
            dcc.Tab(label='Bottom 10', children=[
                dcc.Graph(figure=px.bar(records["Bottom 10"], x="Country", y="GDP",
                                        title="Bottom 10 Countries by GDP",
                                        color="GDP", color_continuous_scale="Reds"))
            ]),
            dcc.Tab(label='Global GDP Trend', children=[
                dcc.Graph(figure=px.line(x=list(records["Global GDP Trend"].keys()),
                                         y=list(records["Global GDP Trend"].values()),
                                         title="Global GDP Trend Over Time"))
            ]),
            dcc.Tab(label='Avg GDP by Continent', children=[
                html.Ul([
                    html.Li(f"{continent}: {avg:,.2f}")
                    for continent, avg in records["Avg GDP by Continent"].items()
                ])
            ]),
            dcc.Tab(label='Growth Rate', children=[
                dcc.Graph(figure=px.bar(
                    x=list(records["Growth Rate"].keys()),
                    y=[round(val, 2) for val in records["Growth Rate"].values()],
                    title="GDP Growth Rates (%)",
                    color=[round(val, 2) for val in records["Growth Rate"].values()],
                    color_continuous_scale="Viridis"
                ))
            ]),
            dcc.Tab(label='Fastest Continent', children=[
                html.Div(f"Fastest Growing Continent: {records['Fastest Continent']}")
            ]),
            dcc.Tab(label='Consistent Decline', children=[
                html.Ul([html.Li(country) for country in records["Consistent Decline"]])
            ]),
            dcc.Tab(label='Continent Contribution', children=[
                dcc.Graph(figure=px.pie(names=list(records["Continent Contribution"].keys()),
                                        values=list(records["Continent Contribution"].values()),
                                        title="Continent Contribution to Global GDP (%)"))
            ])
        ])

        app.layout = html.Div([
            html.H1("GDP Analysis Dashboard"),
            tabs
        ])

        app.run(debug=True)