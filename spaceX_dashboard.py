import dash
import pandas as pd
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

data= pd.read_csv('spacex_launch_dash.csv')

#Unique Launch Sites
all_options=[{'label':'All Sites','value':'all'}]+[{'label':x,'value':x}for x in sorted(data['Launch Site'].unique())]

app.layout = dbc.Container([
    dbc.Row([
        html.H1('SpaceX Launch Records Dashboard',className='text-center fs-2 text fst-normal')
    ]),
    dbc.Row([
        dcc.Dropdown(id='dropdown',value='all',multi=False,
            options=all_options),
        dcc.Graph(id='pie-chart',figure={})
            ]),
    dbc.Row([
        dcc.RangeSlider(min=0, max=data['Payload Mass (kg)'].max(),step =1000, value=[0, data['Payload Mass (kg)'].max()], id='slider'),
        dcc.Graph(id='scatter-plot',figure={})
    ]),

])

@app.callback(
    Output(component_id='pie-chart',component_property='figure'),
    [Input(component_id='dropdown',component_property='value')]
    )

def update_chart(val_chosen):
    print(f'Applying callback Value chosen {val_chosen}')
    if val_chosen == 'all':
        fig = px.pie(data, 
                     values='class', 
                     names='Launch Site', 
                     title=f'Total Success Launches By Site')  
        return fig
        
    else:
        filtered_df = data[data['Launch Site'] == val_chosen]
        filtered_df = filtered_df.groupby('class').count().reset_index()        
        fig = px.pie(filtered_df, 
                     values='class', 
                     names='Launch Site', 
                     title='Total Launches for site {}'.format(val_chosen))        
        return fig

@app.callback(Output(component_id='scatter-plot', component_property='figure'),
              [Input(component_id='dropdown', component_property='value'), 
              Input(component_id="slider", component_property="value")])
def get_scatter_chart(val_chosen, range_chosen):
    if val_chosen == 'all':
        filtered_df = data[(data['Payload Mass (kg)'] >= int(range_chosen[0])) & (data['Payload Mass (kg)'] <= int(range_chosen[1]))]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        filtered_df = data[(data['Launch Site'] == val_chosen) & 
                                (data['Payload Mass (kg)'] >= int(range_chosen[0])) &
                                (data['Payload Mass (kg)'] <= int(range_chosen[1]))
                               ]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    
if __name__ == "__main__":
    app.run_server()