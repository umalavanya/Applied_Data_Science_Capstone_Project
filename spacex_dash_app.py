import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output

# Read the SpaceX launch data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Calculate the maximum and minimum payload values for the slider
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Get unique launch sites for dropdown options
unique_launch_sites = spacex_df["Launch Site"].unique()

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': unique_launch_sites[0], 'value': unique_launch_sites[0]},
                     {'label': unique_launch_sites[1], 'value': unique_launch_sites[1]},
                     {'label': unique_launch_sites[2], 'value': unique_launch_sites[2]},
                     {'label': unique_launch_sites[3], 'value': unique_launch_sites[3]},
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site",
                 searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                     min=0, max=10000, step=1000,
                     marks={0: '0', 100: '100'},
                     value=[min_payload, max_payload]),
    html.Br(),
    dcc.Graph(id='success-payload-scatter-chart'),
])

# Callback for pie chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def update_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, names='class', title='Success vs. Failure for All Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', title=f'Success vs. Failure for {entered_site}')
    return fig

# Callback for scatter chart
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def update_scatter_chart(entered_site, payload_range):
    if entered_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category', title='Payload Mass vs. Launch Success (All Sites)')
    else:
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1]) &
                                (spacex_df['Launch Site'] == entered_site)]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category', title=f'Payload Mass vs. Launch Success ({entered_site})')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
