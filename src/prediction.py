import math
import pickle
import pathlib
import numpy as np
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, callback  # pip install dash (version 2.0.0 or higher)
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

prediction_layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Row(
                    [
                        html.Div([
                            html.P("Please fill your personal health information.",style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'1.5em',}),
                        ])
                        
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Name: "),
                                dbc.Input(id="input_name", placeholder="Type Name", type="text"),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Label("BMI: "),
                                        dbc.Input(id="input_bmi", placeholder="Type BMI", type="text", value=""),
                                        dbc.FormText("Please input number"),
                                        dbc.FormFeedback("Valid", type="valid"),
                                        dbc.FormFeedback("Sorry, it's not a number",type="invalid",),
                                    ]
                                ),

                                html.Br(),
                                html.Label("Gender: "),
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Male", "value": "Male"},
                                        {"label": "Female", "value": "Female"},
                                    ],
                                    id="radio_gender",
                                    inline=True,
                                ),
                                html.Br(),
                                html.Label("Residence Type: "),
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Urban", "value": "Urban"},
                                        {"label": "Rural", "value": "Rural"},
                                    ],
                                    id="radio_rt",
                                    inline=True,
                                ),
                                html.Br(),
                                html.Label("Smoke: "),
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Unknown", "value": "Unknown"},
                                        {"label": "Formerly smoked", "value": "Formerly smoked"},
                                        {"label": "Never smoked", "value": "Never smoked"},
                                        {"label": "Smokes", "value": "Smokes"},
                                    ],
                                    id="radio_smoke",
                                    inline=True,
                                ),
                                html.Br(),
                                html.Label("Work Type: "),
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Private", "value": "Private"},
                                        {"label": "Self-employed", "value": "Self-employed"},
                                        {"label": "Children", "value": "children"},
                                        {"label": "Government Job", "value": "Govt_job"},
                                        {"label": "Never Work", "value": "Never_worked"},
                                    ],
                                    id="radio_wt",
                                    inline=True,
                                ),
                                html.Br(),
                                dbc.Tooltip(
                                    "Body Mass Index (BMI)",
                                    target="input_bmi",
                                ),                                                        
                            ],
                            width = 6,
                        ),
                        dbc.Col(
                            [
                                html.Label("Age: "),
                                dbc.Input(id="input_age", placeholder="Type Age", type="text", value=""),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Label("Average Glucose Level: "),
                                        dbc.Input(id="input_ag", placeholder="Type Avg Glucose", type="text", value=""),
                                        dbc.FormText("Please input number"),
                                        dbc.FormFeedback("Valid", type="valid"),
                                        dbc.FormFeedback("Sorry, it's not a number",type="invalid",),
                                    ]
                                ),
                                html.Br(),
                                html.Label("Hypertension: "),
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Yes", "value": "Yes"},
                                        {"label": "No", "value": "No"},
                                    ],
                                    id="radio_hypertension",
                                    inline=True,
                                ),
                                html.Br(),
                                html.Label("Heart Disease: "),
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Yes", "value": "Yes"},
                                        {"label": "No", "value": "No"},
                                    ],
                                    id="radio_hd",
                                    inline=True,
                                ),
                                html.Br(),
                                html.Label("Ever Married: "),
                                dbc.RadioItems(
                                    options=[
                                        {"label": "Yes", "value": "Yes"},
                                        {"label": "No", "value": "No"},
                                    ],
                                    id="radio_em",
                                    inline=True,
                                ),
                                html.Br(),
                                dbc.Tooltip(
                                    "Have you gotten high blood pressure before?",
                                    target="radio_hypertension",
                                ),
                                dbc.Tooltip(
                                    "Have you gotten any heart disease before?",
                                    target="radio_hd",
                                ),
                                dbc.Tooltip(
                                    "Have you ever been married?",
                                    target="radio_em",
                                ),   
                            ],   
                            width = 6,
                        )
                    ]
                ),
            ],
            className="mt-4",
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Row(
                    [
                        html.P("Health Report", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2.5em', 'text-align':'center'})
                    ]
                ),
                dbc.Row(
                    [
                        html.Hr(style={"borderWidth": "0.7vh", "width": "100%", "borderColor": "gray","opacity": "unset",})
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div([
                                    html.P("Name:", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2em', 'display': 'inline-block'}),
                                    html.Span(id="spanName", style={'font':'Monospace', 'font-size':'1.5em', 'display': 'inline-block', "margin-left": "15px", "color":"#7B8FA1"}),
                                ])
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Div([
                                    html.P("Age:", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2em', 'display': 'inline-block'}),
                                    html.Span(id="spanAge", style={'font':'Monospace', 'font-size':'1.5em', 'display': 'inline-block', "margin-left": "15px", "color":"#7B8FA1"}),
                                ])
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Div([
                                    html.P("Gender:", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2em', 'display': 'inline-block'}),
                                    html.Span(id="spanGender", style={'font':'Monospace', 'font-size':'1.5em',  'display': 'inline-block', "margin-left": "15px", "color":"#7B8FA1"}),
                                ])
                            ]
                        ),

                    ]
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div([
                                    html.P("Hypertension:", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2em', 'display': 'inline-block'}),
                                    html.Span(id="spanHypertension", style={'font':'Monospace', 'font-size':'1.5em', 'display': 'inline-block', "margin-left": "15px"}),
                                ]),
                                html.Div([
                                    html.P("Heart Disease:", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2em', 'display': 'inline-block'}),
                                    html.Span(id="spanHd", style={'font':'Monospace', 'font-size':'1.5em', 'display': 'inline-block', "margin-left": "15px"}),
                                ]),
                                html.Div([
                                    html.P("Ever Married:", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2em', 'display': 'inline-block'}),
                                    html.Span(id="spanEm", style={'font':'Monospace', 'font-size':'1.5em', 'display': 'inline-block', "margin-left": "15px"}),
                                ]),

                            ]
                        ),
                        dbc.Col(
                            [
                                html.Div([
                                    html.P("Work Type:", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2em', 'display': 'inline-block'}),
                                    html.Span(id="spanWt", style={'font':'Monospace', 'font-size':'1.5em', 'display': 'inline-block', "margin-left": "15px", "color": "#5dacbd"}),
                                ]),
                                html.Div([
                                    html.P("Smoke", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2em', 'display': 'inline-block'}),
                                    html.Span(id="spanSmoke", style={'font':'Monospace', 'font-size':'1.5em', 'display': 'inline-block', "margin-left": "15px", "color": "#5dacbd"}),
                                ]),
                                html.Div([
                                    html.P("Residence Type:", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2em', 'display': 'inline-block'}),
                                    html.Span(id="spanRt", style={'font':'Monospace', 'font-size':'1.5em', 'display': 'inline-block', "margin-left": "15px", "color": "#5dacbd"}),
                                ]),
                                
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        html.Hr(style={"borderWidth": "0.7vh", "width": "100%", "borderColor": "gray","opacity": "unset",})
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.P("BMI:", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2em', 'display': 'inline-block'}),
                                    ], width = 4
                                ),
                                dbc.Col(
                                    [
                                        html.Br(),
                                        dbc.Progress(id="bar_bmi"),
                                        
                                    ], width = 8
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.P("Average Glucose:", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2em', 'display': 'inline-block'}),
                                    ], width = 4
                                ),
                                dbc.Col(
                                    [
                                        html.Br(),
                                        dbc.Progress(id="bar_ag"),
                                        
                                    ], width = 8
                                )
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        html.Hr(style={"borderWidth": "0.7vh", "width": "100%", "borderColor": "gray","opacity": "unset",})
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Row(
                            [
                                html.Div([
                                html.P("Stroke Risk :", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2em', 'display': 'inline-block'}),
                                ]), 
                            ]
                        ),
                        dbc.Row(
                            [
                                html.Span(id="stroke_risk", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'3.5em', 'text-align':'center', "margin-left": "15px"}),
                            ]
                        ),
                        dbc.Row(
                            [
                                html.Div([
                                html.P("What you can do :", style={'font':'Monospace', 'font-weight': 'bold', 'font-size':'2em', 'display': 'inline-block'}),
                                ]),
                                html.Span(id="advice", style={'font':'Monospace', 'font-size':'1.5em', 'display': 'inline-block', "margin-left": "15px", "color": "#5dacbd"}),
                            ]
                        ),
                    ]
                ),
                
            ],
            style={"border":"5px solid", "border-radius" : "25px", "padding":'30px', "margin-left":"150px", "margin-right":"150px"}, className='mb-4'
        ),
        dcc.Store(id='pred_res', data=[], storage_type='memory'),
    ]
)

tmp = ["input_bmi", "input_ag"]
for element in tmp:
    @callback(
        [Output(element, "valid"), Output(element, "invalid")],
        [Input(element, "value")],
    )
    def check_validity(text):
        if len(text) != 0 and text.isnumeric():
            return True, False
        elif len(text) != 0 and not text.isnumeric():
            return False, True
        return False, False

pass_out_components=["spanName", "spanAge", "spanGender", "spanSmoke", "spanWt", "spanRt"]
pass_in_components=["input_name", "input_age", "radio_gender", "radio_smoke", "radio_wt", "radio_rt"]
for i, out_component in enumerate(pass_out_components):
    @callback(
        Output(component_id=out_component, component_property="children"),
        Input(component_id=pass_in_components[i], component_property="value"),  
    )
    def passValue(text):
        return text

component_ids = [ "spanHypertension", "spanHd", "spanEm"]
input_ids = ["radio_hypertension", "radio_hd", "radio_em"]
color_map = {"Yes": "#F48484", "No": "#AACB73"}

for i, component_id in enumerate(component_ids):
    @callback(
        Output(component_id=component_id, component_property="children"),
        Output(component_id=component_id, component_property="style"),
        Input(component_id=input_ids[i], component_property="value"),
        State(component_id, "style"),  
    )
    def update_text_and_style(text, current_style):
        if text in color_map:
            new_style = {'color': color_map[text]}
            update_style = {**current_style, **new_style}
            return text, update_style
        else:
            return "", current_style


@callback(
    Output(component_id="bar_bmi", component_property="label"),
    Output(component_id="bar_bmi", component_property="value"),
    Input(component_id="input_bmi", component_property="value"),  
)
def generate_bar_bmi(input_1):
    if len(input_1) == 0:
        return input_1, 0
    else:
        return input_1, int(input_1)/50*100

@callback(
    Output(component_id="bar_ag", component_property="label"),
    Output(component_id="bar_ag", component_property="value"),
    Input(component_id="input_ag", component_property="value"),  
)
def generate_bar_sleep(input_1):
    if len(input_1) == 0:
        return input_1, 0
    else:
        return input_1, int(input_1)/200*100
    


@callback(
    Output(component_id="pred_res", component_property="data"),
    Input(component_id="radio_hypertension", component_property="value"),
    Input(component_id="radio_hd", component_property="value"),  
    Input(component_id="radio_em", component_property="value"),  
    Input(component_id="radio_gender", component_property="value"),  
    Input(component_id="radio_rt", component_property="value"), 
    Input(component_id="radio_wt", component_property="value"),
    Input(component_id="radio_smoke", component_property="value"), 
    Input(component_id="input_bmi", component_property="value"),
    Input(component_id="input_ag", component_property="value"), 
    Input(component_id="input_age", component_property="value"),
)
def prediction(input1, input2, input3, input4, input5, input6, input7, input8, input9, input10):
    para = [input1, input2, input3, input4, input5, input6, input7, input8, input9, input10]
    for i in range(0, 3):
        if para[i] != None and para[i] == "Yes":
            para[i] = 1
        else:
            para[i] = 0

    if para[3] != None and para[3] == "Female":
        para[3] = 0
    else:
        para[3] = 1

    if para[4] != None and para[4] == "Urban":
        para[4] = 1
    else:
        para[4] = 0

    work_type = {'Govt_job':0, 'Never_worked':1, 'Private':2, 'Self-employed':3, 'children':4}
    if para[5] == None:
        para[5] = 0
    elif para[5] in work_type:
        para[5] = work_type[para[5]]
    
    smoke = {'Unknown':0, 'Formerly smoked':1, 'Never smoked':2, 'Smokes':3}
    if para[6] == None:
        para[6] = 0
    elif para[6] in smoke:
        para[6] = smoke[para[6]]

    for i in range(7,10):
        if len(para[i]) == 0:
            para[i] = 0
        else:
            para[i] = int(para[i])

    test = [para[3], para[-1], para[0], para[1], para[2], para[5], para[4], para[8], para[7], para[6]]
    res = np.array(test).reshape(1, -1)

    with open('SVCModel.pkl', 'rb') as f:
        model = pickle.load(f)
        prediction = model.predict(res)

    if para[-1] > 70 or para[-2] > 150 or prediction == 1:
        return "HIGH"
    else:
        return "LOW"


color_prediction = {"HIGH": "#F48484", "LOW": "#AACB73"}   
@callback(
    Output(component_id="stroke_risk", component_property="children"),
    Output(component_id="stroke_risk", component_property="style"),
    Input(component_id="pred_res", component_property="data"),
    State("stroke_risk", "style"),  
)
def update_text_and_style(text, current_style):
    if text in color_prediction:
        new_style = {'color': color_prediction[text]}
        update_style = {**current_style, **new_style}
        return text, update_style
    else:
        return "", current_style

input_list = ["radio_hypertension", "radio_hd", "radio_smoke", "input_bmi", "input_ag"]
suggestions = ["Please limit sodium intake and alcohol consumption.",
               "Please contact your doctor to eliminate the chance of heart disease.",
               "Please reduce the amount of smoking.",
               "Your BMI is too high, please do exercise regularly and keep healthy dietary.",
               "Please reduce the sugar intake to keep balance glucose level."]

@callback(
    Output(component_id="advice", component_property="children"),
    [Input(component_id=input, component_property="value") for input in input_list]
)
def update_span_text(*input_values):
    spans = []
    for index, input_value in enumerate(input_values):
        if index == 2:
            if input_value != None and input_value != "Unknown":
                spans.append(html.Span(suggestions[index]))
                spans.append(html.Br())
            else:
                 spans.append(html.Span())
        elif index == 3:
            if len(input_value) != 0 and int(input_value) >= 40:
                spans.append(html.Span(suggestions[index]))
                spans.append(html.Br())
            else:
                 spans.append(html.Span())
        elif index == 4:
            if len(input_value) != 0 and int(input_value) > 100:
                spans.append(html.Span(suggestions[index]))
                spans.append(html.Br())
            else:
                 spans.append(html.Span())
        else:                                         
            if input_value == "Yes":
                spans.append(html.Span(suggestions[index]))
                spans.append(html.Br())
            else:
                spans.append(html.Span())
    return spans