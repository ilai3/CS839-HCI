import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback  # pip install dash (version 2.0.0 or higher)
import dash_bootstrap_components as dbc

TEAGE_images = [
    html.Img(src=r'assets/Ridge Regression_TEAGE.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/Lasso Regression_TEAGE.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/Random Forest_TEAGE.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/XGBoost_TEAGE.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/MLP_TEAGE.png', alt='image', style={'height':'50%', 'width':'50%'})
]
    
TRCHILDNUM_images = [
    html.Img(src=r'assets/Ridge Regression_TRCHILDNUM.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/Lasso Regression_TRCHILDNUM.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/Random Forest_TRCHILDNUM.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/XGBoost_TRCHILDNUM.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/MLP_TRCHILDNUM.png', alt='image', style={'height':'50%', 'width':'50%'})
]

TRYHHCHILD_images = [
    html.Img(src=r'assets/Ridge Regression_TRYHHCHILD.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/Lasso Regression_TRYHHCHILD.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/Random Forest_TRYHHCHILD.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/XGBoost_TRYHHCHILD.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/MLP_TRYHHCHILD.png', alt='image', style={'height':'50%', 'width':'50%'})
]

TEHRUSLT_images = [
    html.Img(src=r'assets/Ridge Regression_TEHRUSLT.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/Lasso Regression_TEHRUSLT.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/Random Forest_TEHRUSLT.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/XGBoost_TEHRUSLT.png', alt='image', style={'height':'50%', 'width':'50%'}), 
    html.Img(src=r'assets/MLP_TEHRUSLT.png', alt='image', style={'height':'50%', 'width':'50%'})
]

TEAGE_df = pd.DataFrame(
    {
        "Model Name": ["Ridge", "Lasso", "Random Forest", "XGBoost", "MLP (100)"],
        "RMSE": [16.6409, 16.6435, 16.3329, 16.2926, 16.3596],
        "MSE": [276.918, 277.0075, 266.7637, 265.448, 267.6379],
        "R-Squared Score": [0.1477, 0.1474, 0.1789, 0.183, 0.1762],
        "Scatter Plot": TEAGE_images
    }
)

TRCHILDNUM_df = pd.DataFrame(
    {
        "Model Name": ["Ridge", "Lasso", "Random Forest", "XGBoost", "MLP (100)"],
        "RMSE": [1.0348, 1.0569, 1.0344, 1.0299, 1.0251],
        "MSE": [1.0709, 1.117, 1.0701, 1.0608, 1.0509],
        "R-Squared Score": [0.0946, 0.0556, 0.0953, 0.1031, 0.1115],
        "Scatter Plot": TRCHILDNUM_images
    }
)

TRYHHCHILD_df = pd.DataFrame(
    {
        "Model Name": ["Ridge", "Lasso", "Random Forest", "XGBoost", "MLP (100)"],
        "RMSE": [5.2046, 5.2243, 5.1147, 5.1294, 5.0973],
        "MSE": [27.0878, 27.2934, 26.1601, 26.3104, 25.9821],
        "R-Squared Score": [0.0341, 0.0267, 0.0671, 0.0618, 0.0735],
        "Scatter Plot": TRYHHCHILD_images
    }
)

TEHRUSLT_df = pd.DataFrame(
    {
        "Model Name": ["Ridge", "Lasso", "Random Forest", "XGBoost", "MLP (100)"],
        "RMSE": [15.9472, 15.9528, 15.8366, 15.836, 15.8271],
        "MSE": [254.3126, 254.4907, 250.7995, 250.7797, 250.4986],
        "R-Squared Score": [0.0447, 0.0441, 0.0579, 0.058, 0.059],
        "confusion matrix": TEHRUSLT_images
    }
)
    
regression_layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("Regression Models")
        ], width=12),
        
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id="attr",
                options=[
                    {"label": "TEAGE", "value": "age"},
                    {"label": "TRCHILDNUM", "value": "childnum"},
                    {"label": "TRYHHCHILD", "value": "age_child"}, 
                    {"label": "TEHRUSLT", "value": "hours"},
                ],
                multi=False,
                value="age",
                clearable=False,
                style={'width': "40%", 'float':'right'},
                className='form-dropdown',
                ),
        ], width = 12),
    ], className='mb-4'),

    dbc.Row([
        dbc.Col([
             dcc.Graph(id='RMSE')
        ], width=4),
        dbc.Col([
             dcc.Graph(id='MSE')
        ], width=4),
        dbc.Col([
             dcc.Graph(id='R2')
        ], width=4),
    ],style={"border":"2px solid", "border-radius" : "25px", "color" : "#66B3FF", "padding":'5px'}, className='mb-4'),
    dbc.Row([
        dbc.Col(id="table", width=12),
    ]),
    
])
@callback(
    Output(component_id='RMSE', component_property='figure'),
    Output(component_id='MSE', component_property='figure'),
    Output(component_id='R2', component_property='figure'),
    [Input(component_id='attr', component_property='value')]
)
def update_model_graph(option_atr):
    if option_atr == 'age':
        age_df = TEAGE_df
        rmse_barchart=px.bar(
            data_frame=age_df,
            x="Model Name",
            y="RMSE",
            color="Model Name",
        )
        mse_barchart=px.bar(
            data_frame=age_df,
            x="Model Name",
            y="MSE",
            color="Model Name",
        )
        r2_barchart=px.bar(
            data_frame=age_df,
            x="Model Name",
            y="R-Squared Score",
            color="Model Name",
        )
        return rmse_barchart, mse_barchart, r2_barchart
    if option_atr == 'childnum':
        children_df = TRCHILDNUM_df
        rmse_barchart=px.bar(
            data_frame=children_df,
            x="Model Name",
            y="RMSE",
            color="Model Name",
        )
        mse_barchart=px.bar(
            data_frame=children_df,
            x="Model Name",
            y="MSE",
            color="Model Name",
        )
        r2_barchart=px.bar(
            data_frame=children_df,
            x="Model Name",
            y="R-Squared Score",
            color="Model Name",
        )
        return rmse_barchart, mse_barchart, r2_barchart
    if option_atr == 'age_child':
        age_child_df = TRYHHCHILD_df
        rmse_barchart=px.bar(
            data_frame=age_child_df,
            x="Model Name",
            y="RMSE",
            color="Model Name",
        )
        mse_barchart=px.bar(
            data_frame=age_child_df,
            x="Model Name",
            y="MSE",
            color="Model Name",
        )
        r2_barchart=px.bar(
            data_frame=age_child_df,
            x="Model Name",
            y="R-Squared Score",
            color="Model Name",
        )
        return rmse_barchart, mse_barchart, r2_barchart
    if option_atr == 'hours':
        hours_df = TEHRUSLT_df
        rmse_barchart=px.bar(
            data_frame=hours_df,
            x="Model Name",
            y="RMSE",
            color="Model Name",
        )
        mse_barchart=px.bar(
            data_frame=hours_df,
            x="Model Name",
            y="MSE",
            color="Model Name",
        )
        r2_barchart=px.bar(
            data_frame=hours_df,
            x="Model Name",
            y="R-Squared Score",
            color="Model Name",
        )
        return rmse_barchart, mse_barchart, r2_barchart

@callback(
    Output(component_id='table', component_property='children'),
    [Input(component_id='attr', component_property='value')]
)
def update_graph(option_atr):
    if option_atr == "age":
        return dbc.Table.from_dataframe(TEAGE_df, striped=True, bordered=True, hover=True, color="primary", style={'text-align': 'center', 'vertical-align':'middle'},)
    if option_atr == "childnum":
        return dbc.Table.from_dataframe(TRCHILDNUM_df, striped=True, bordered=True, hover=True, color="primary", style={'text-align': 'center', 'vertical-align':'middle'},)
    if option_atr == "age_child":
        return dbc.Table.from_dataframe(TRYHHCHILD_df, striped=True, bordered=True, hover=True, color="primary", style={'text-align': 'center', 'vertical-align':'middle'},)
    if option_atr == "hours":
        return dbc.Table.from_dataframe(TEHRUSLT_df, striped=True, bordered=True, hover=True, color="primary", style={'text-align': 'center', 'vertical-align':'middle'},)






