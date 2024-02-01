import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.4) pip install plotly==4.5.4
import plotly.express as px

import dash             #(version 1.9.1) pip install dash==1.9.1
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv('/workspaces/codespaces-blank/Employees Revised.csv')

app.layout = html.Div([
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=df.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
            ],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 6,
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            # virtualization=False,
            style_cell_conditional=[
                {'if': {'column_id': 'City'},
                 'width': '40%', 'textAlign': 'left'},
                {'if': {'column_id': 'JobTitle'},
                 'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'Gender'},
                 'width': '30%', 'textAlign': 'left'},		
                {'if': {'column_id':'AbsentHours'},
                 'width': '30%', 'textAlign': 'left'},
            ],
        ),
    ],className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='bardropdown',
                options=[
                         {'label': 'Cities', 'value': 'City'},
                         {'label': 'Jobs', 'value': 'JobTitle'},			
                         {'label': 'Gender', 'value': 'Gender'},
			             {'label': 'Absent_Hours', 'value': 'AbsentHours'},

                ],
                value='City',
                multi=False,
                clearable=False
            ),
        ],className='six columns'),

        html.Div([
        dcc.Dropdown(id='piedropdown',
            options=[
                     {'label': 'Cities', 'value': 'City'},
                     {'label': 'Jobs', 'value': 'JobTitle'},			
                     {'label': 'Gender', 'value': 'Gender'},
			         {'label': 'Absent_Hours', 'value': 'AbsentHours'},
            ],
            value='JobTitle',
            multi=False,
            clearable=False
        ),
        ],className='six columns'),

    ],className='row'),

    html.Div([
        html.Div([
            dcc.Graph(id='barchart'),
        ],className='six columns'),

        html.Div([
            dcc.Graph(id='piechart'),
        ],className='six columns'),

    ],className='row'),


])


@app.callback(
    [Output('piechart', 'figure'),
     Output('barchart', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('bardropdown', 'value')]
)
def update_data(chosen_rows, piedropval, bardropval):
    if len(chosen_rows)==0:
        df_filterd = df[df['City'].isin(['Vancouver','Victoria','New Westminster','Burnaby'])]
    else:
        print(chosen_rows)
        df_filterd = df[df.index.isin(chosen_rows)]

    pie_chart=px.pie(
            data_frame=df_filterd,
            names='City',
            values=piedropval,
            hole=.3,
            labels={'':'Cities'}
            )


    #extract list of chosen cities
    list_chosen_cities = df_filterd['City'].tolist()    
    print (df[:5])
    df_bar = df[df['City'].isin(list_chosen_cities)]

    bar_chart = px.bar(
            data_frame=df_bar,
            x='JobTitle',
            y=bardropval,
            color='Gender',
            labels={'City':'Cities','JobTitle':'Jobs'},
            )
    bar_chart.update_layout(uirevision='foo')

    return (pie_chart,bar_chart)



if __name__ == '__main__':
    app.run_server(debug=True)