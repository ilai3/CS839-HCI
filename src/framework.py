import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

framework_layout = html.Div([
    dbc.Row([
        html.Img(src='assets/framework.jpeg', style={"width":"70%", "height" : "70%", "display":"block", "margin-left":"auto", "margin-right":"auto"})
    ])
])


