'''
    InteractiveMap serves to create an Interactive Map using plotly and should
    be used to return the HTML code that can then be inserted as a child of the
    dash app layout.
    Last Updated: November 23, 2020
'''
import ast
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

def create_building_average_plot():
    '''Returns a plotly figure containing buildings and hoverdata for their last 24 hour hourly average energy consumption.'''

    # Prefix/suffix to be used in combination with later extracted label name to define relative pathing.
    prefix_file_path = "./data/Analysis/"
    suffix_file_path = "_results.csv"
    plotly_configuration = {"displaylogo" : False,
                            "scrollZoom" : False,
                            "displayModeBar" : False,
                            }
    # Initializing Figure and data.
    figure = go.Figure()
    df_geography = pd.read_csv("./data/Geography/geography_data.csv", header = 0, index_col = 0)
    # ast.literal_eval required to cast string type to list type.
    df_geography.latitude = df_geography.latitude.apply(lambda x: ast.literal_eval(x))
    df_geography.longitude = df_geography.longitude.apply(lambda x: ast.literal_eval(x))
    for index, row  in df_geography.iterrows():
        # We need to recreate the filepath from the key_name due to varying format, standardized formatting would void this requirement.
        file_name = ""
        for alpha in row["key_name"]:
            file_name += "" if (alpha == "\xa0" or alpha == "'" or alpha == " ") else alpha
        # Try/except allows us to display the graphs for which we have data to show.
        try:
            df_stat_data = pd.read_csv(prefix_file_path + file_name + suffix_file_path)
        except:
            continue
        avg_24_hr_actual = df_stat_data.Actual[-24:].mean()
        avg_24_hr_predicted = df_stat_data.Predicted[-24:].mean()
        figure.add_trace(
            go.Scattermapbox(
                # Fill inner area.
                fill = "toself",
                fillcolor = "#ffb71b",
                # Properties for the display box that appears when hovering over graph traces.
                hoverlabel = {"bgcolor" : "#bec0c2",
                              "bordercolor" : "#0f2044",
                              "font" : {"family" : "Sofia Pro",
                                        "color" : "black"},
                              },
                # Description that appears within the hover box, <br> is used to end the line.
                hovertemplate = "{}<br>Actual Average: {:.2f}<br>Predicted Average: {:.2f}"\
                .format(row["name"], avg_24_hr_actual, avg_24_hr_predicted),
                lat = row["latitude"],
                lon = row["longitude"],
                # Trace colour.
                marker = {"color" : "#0f2044"},
                # Traces in a continuous line.
                mode = "lines",
                # Prevents additional hoverbox from appearing. 
                name = "",
                )
            )
    figure.update_layout(width = 1020,
                         height = 720,
                         # Determines the properties of the actual background map.
                         mapbox_style = "carto-positron",
                         # Sets where the plot is centered at.
                         mapbox = {"center" : {"lat" : 36.0685,
                                               "lon" : -79.8101,
                                               },
                                   "zoom" : 15.5,
                                   },
                         # Margin 0 prevents any whitespace.
                         margin = {"l" : 0,
                                   "r" : 0,
                                   "b" : 0,
                                   "t" : 0},
                         # Turns off/on side panel that displays legend.
                         showlegend = False,
                         )

    return figure, plotly_configuration
	
def return_html_def_building_plot():
    '''Returns the html definition for the interactive building plot to be inserted as a child of a dash app layout.'''
    # Retrieves the interactive plotly figure and the configuration info.
    figure, plotly_configuration = create_building_average_plot()
    html_def = html.Center([
        dbc.Container(html.Center(html.H3("UNCG Daily Energy Consumption", id='top', className = "mt-2"))),
        dcc.Graph(
            id = "interactive_map",
            figure = figure,
            config = plotly_configuration
            ),
        html.Br(),
        ]
    )
    return html_def
