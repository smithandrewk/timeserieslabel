#! /usr/bin/env python3
import json

from dash import Dash, dcc, html,ctx
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sys

def write_data_dot_json(data):
    with open(f'data2.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def get_data_dot_json():
    import os
    if(os.path.isfile(f'data2.json')):
        print('data2.json exists')
        with open(f'data2.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        print('data2.json does not exist')
        data = {}
        with open(f'data2.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    return data
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
colormap = {
    'Eating':'green',
    'NONE':'black',
    'Smoking':'red',
    'Jogging':'blue',
    'Medication':'yellow',
    'Exercise':'blue',
    'General':'black',
    'PILL':'yellow'
}
df = pd.read_csv(f'data2.csv')
data_json = get_data_dot_json()
df = df.iloc[data_json['start']:data_json['end'],:]
fig = px.scatter(data_frame=df,y='acc_x')
fig.update_traces(marker_size=6)
for bout in data_json['puffs']:
    fig.add_vrect(x0=bout['start'], x1=bout['end'], fillcolor='red', opacity=.1)

fig.update_layout(clickmode='event+select')
current_bout_selected = 0
app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig,
        style={'width': '90vw', 'height': '90vh'}
    ),
],style={
    'display':'flex',
    'flex-direction':'column',
    'align-items':'center',
})


    
if __name__ == '__main__':
    app.run_server(debug=True,port=5050)
