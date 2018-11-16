import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import re
import random


# csv_file = requests.get('https://raw.githubusercontent.com/chudianya/kit_sponsors_plotly/blob/master/kit_sponsors_real.csv')
df = pd.read_csv("https://raw.githubusercontent.com/chudianya/kit_sponsors_plotly/master/kit_sponsors_real.csv")

cols = [re.sub(r"\-\d+","",day) for day in df.columns]
cols_dict = {re.sub(r"\-\d+","",year): year for year in df.columns}
get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF),range(n)))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children='''
        Premier League Kit Manufacturers since 2014
    '''),

  dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min= 0,
        max=len(cols),
        value=0,
        marks={i: str(year) for i, year in enumerate(cols)}
    )
])


@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')],
    [dash.dependencies.State('year-slider','marks')])

def update_figure(selected_year,marks):
    seleb = marks[str(selected_year)]
    filtered_df = df.loc[:,cols_dict[seleb]].value_counts().to_frame()
    trace = []
    trace.append(go.Bar(
        x=list(filtered_df.index),
        y=list(filtered_df.iloc[:,0]),
        marker=dict(
        color= get_colors(13))
      
        
    ))

    return {
        'data': trace,
        'layout': go.Layout(
            xaxis={'title': 'Kit Sponsor'},
            yaxis={'title': 'Number of clubs sponsored', 'range': [0, 6]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)