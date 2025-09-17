# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(
                                 id='site-dropdown',
                                 # List of option dictionaries: one for "All Sites" + one per unique site
                                 options=[{'label': 'All Sites', 'value': 'ALL'}] +
                                           [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                 # Default value
                                 value='ALL',
                                 # Placeholder text description
                                 placeholder='Select a Launch Site here',
                                 # Enable searching inside dropdown
                                 searchable=True
                                ),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                  id='payload-slider',
                                  min=0,               # slider starting point (Kg)
                                  max=10000,           # slider ending point (Kg)
                                  step=1000,           # interval step size (Kg)
                                  value=[min_payload, max_payload],  # default range from min to max payload in dataset
                                  marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},  # optional ticks
                                  tooltip={"placement": "bottom", "always_visible": True}  # optional usability feature
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def update_pie_chart(selected_site):
    # If ALL sites selected, show success counts for all sites
    if selected_site == 'ALL':
        # Count number of successes (class=1) for each site
        fig = px.pie(spacex_df, 
                names='Launch Site', 
                values='class',
                title='Total Success Launches by Site')
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Show success vs failure counts for that site
        fig = px.pie(filtered_df, 
                        names='class', 
                        title=f'Total Launch Outcomes for site {selected_site}')
    return fig

# TASK 4:
# Add a callback function for success-payload-scatter-chart

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter(selected_site, payload_range):
    # Extract slider range
    low, high = payload_range
    # Filter dataframe by payload range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]

    if selected_site == 'ALL':
        # Show all sites, color by booster version
        fig = px.scatter(filtered_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for All Sites')
    else:
        # Filter by selected site
        site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(site_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
