# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

site_label = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', 
                                options = [{'label': 'All Sites', 'value': 'ALL'}, 
                                {'label': site_label[0], 'value': site_label[0]},
                                {'label': site_label[1], 'value': site_label[1]},
                                {'label': site_label[2], 'value': site_label[2]},
                                {'label': site_label[3], 'value': site_label[3]},],
                                value = 'ALL',
                                placeholder = "Select a Launch Site here",
                                searchable= True
                                ),
   
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                # Function decorator to specify function input and output
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000, 
                                marks={0: '0', 2500: '2500',
                                5000: '5000', 7500:'7500', 10000:'10000'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby('class').count()
    filtered_df = filtered_df.reset_index().iloc[:,0:2].rename(columns = {'Flight Number': 'count'})
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names= 'Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(filtered_df, values='Unnamed: 0', 
        names= 'class', 
        title='Total Success Launches For Site ' + entered_site)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
[Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, entered_payload):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] < entered_payload[1]) &
    (spacex_df['Payload Mass (kg)'] > entered_payload[0])]
    #filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby('class').count()
    #filtered_df = filtered_df.reset_index().iloc[:,0:2].rename(columns = {'Flight Number': 'count'})
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", 
        color ='Booster Version Category', title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", 
        color ='Booster Version Category', title='Total Success Launches By Site2')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()