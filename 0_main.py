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
    df = df.drop([1,5,6,7,8,10],axis=1)
    df = df.rename(mapper={0:'timestamp',2:'x',3:'y',4:'z',9:'label'},axis=1)
    df['timestamp'] = df['timestamp'] - df['timestamp'][0]
    df['timestamp'] = df['timestamp'].astype('datetime64[ns]')
    data = {
        'bouts':[]
    }
    start = 0
    current_label = 0
    for i,label in enumerate(df['label']):
        if(i==0):
            current_label = label
        if(label != current_label):
            data['bouts'].append({'start':start,'end':i-1,'label':current_label})
            current_label = label
            start = i
        if(i == len(df)-1):
            data['bouts'].append({'start':start,'end':i,'label':current_label})
    df = df.drop('label',axis=1)
    return df,data
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
df,data = load_raw_data(filename)

fig = px.scatter(data_frame=df,y=['x','y','z'])
fig.update_traces(marker_size=6)
for bout in data['bouts']:
    fig.add_vrect(x0=bout['start'], x1=bout['end'], annotation_text=bout['label'], annotation_position="top left", annotation=dict(font_size=20, font_family="Times New Roman"), fillcolor=colormap[bout['label']], opacity=.1)

fig.update_layout(clickmode='event+select')
current_bout_selected = 0
app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig,
        style={'width': '90vw', 'height': '90vh'}
    ),
    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Selecting Smoking Session**

                Click on one data point then write beginning and end of session.
            """),
            html.Button('Write Beggining Smoking Session',id='write_beginning_session',n_clicks=0),
            html.Button('Write Ending Smoking Session',id='write_ending_session',n_clicks=0),
            html.Pre(id='selected-data', style=styles['pre'])
    ]),
    ],style={
        'display':'flex',
        'justify-content':'center'
    }),

],style={
    'display':'flex',
    'flex-direction':'column',
    'align-items':'center',
})

@app.callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'),
    Input('write_beginning_session', 'n_clicks'),
    Input('write_ending_session', 'n_clicks'))
def display_selected_data(selectedData,n_clicks,n_clicks_ending):
    trigger = ctx.triggered_id
    print(f'triggered by {trigger}')
    if(selectedData is None):
        print('selected data is none')
        return json.dumps(selectedData, indent=2)
    print(selectedData)
    if(trigger == 'write_beginning_session'):
        data = get_data_dot_json()
        data['start'] = selectedData['points'][0]['x']
        write_data_dot_json(data)
    elif(trigger == 'write_ending_session'):
        data = get_data_dot_json()
        data['end'] = selectedData['points'][0]['x']
        write_data_dot_json(data)
    return json.dumps(selectedData, indent=2)
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
    
if __name__ == '__main__':
    app.run_server(debug=True,port=5050)
