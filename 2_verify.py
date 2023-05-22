#! /usr/bin/env python3
import json

from dash import Dash, dcc, html,ctx
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sys

if len(sys.argv) != 2:
    print('usage: python3 main.py <fileindex>')
    exit(0)

filename = sys.argv[1]

def load_raw_data(fileindex):
    df = pd.read_csv(f'data/{fileindex}/raw_data.csv',header=None)
    df = df.drop([1,3,4,5,6,7,8,10],axis=1)
    df = df.rename(mapper={0:'timestamp',2:'x',3:'y',4:'z',9:'label'},axis=1)
    df['timestamp'] = df['timestamp'] - df['timestamp'][0]
    df['timestamp'] = df['timestamp'].astype('datetime64[ns]')
    df = df.drop('label',axis=1)
    return df
def write_data_dot_json(data):
    global filename
    with open(f'data/{filename}/{filename}_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def get_data_dot_json():
    import os
    if(os.path.isfile(f'data/{filename}/{filename}_data.json')):
        print('data.json exists')
        with open(f'data/{filename}/{filename}_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        print('data.json does not exist')
        data = {}
        with open(f'data/{filename}/{filename}_data.json', 'w', encoding='utf-8') as f:
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
df = load_raw_data(filename)
data_json = get_data_dot_json()
fig = px.scatter(data_frame=df,y='x')
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
