import ast
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

plotly_configuration = {"displaylogo" : False,
                        "scrollZoom" : True,
                        "displayModeBar" : False,
                        }
# Instantiating Map
figure = go.Figure()
df_geography = pd.read_csv("./data/geography/geography_data.csv")

df_geography.latitude = df_geography.latitude.apply(lambda x: ast.literal_eval(x))
df_geography.longitude = df_geography.longitude.apply(lambda x: ast.literal_eval(x))
for index, row  in df_geography.iterrows():
    figure.add_trace(go.Scattermapbox(mode = "lines",
                                      fill = "toself",
                                      fillcolor = "#ffb71b",
                                      lat = row["latitude"],
                                      lon = row["longitude"],
                                      marker = {"size" : 10,
                                                "color" : "#0f2044"},
                                      text = "{}".format(row["name"]),
                                      name = "",
                                      hovertext = "{}".format(row["name"]),
                                      hoverlabel = {"bgcolor" : "#bec0c2",
                                                    "bordercolor" : "#0f2044",
                                                    "font" : {"family" : "Sofia Pro",
                                                              "color" : "black"},
                                                    },
                                      #customdata =,
                                      hovertemplate = "{}".format(row["name"]),
                                      )
                     )


figure.update_layout(height = 800,
                     mapbox_style = "carto-positron",
                     mapbox = {"center" : {"lat" : 36.0676,
                                           "lon" : -79.8101,
                                           },
                               "zoom" : 15,
                               },
                     width = 800,
                     showlegend = False,
                     )


# Dash code
app = dash.Dash(__name__)
app.layout = html.Div([
        dcc.Graph(id = "graph_map_layout",
                  figure = figure,
                  config = plotly_configuration,
                  ),
        ]
    )

def main():
    #app.run_server(debug=True)
    app.run_server(host = "0.0.0.0")
main()
