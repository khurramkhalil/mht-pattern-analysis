import pandas as pd
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from international_border import load_boundaries
from pakistan_polygon import load_polygon
# from server import iterate
import pickle
import socket

app = Dash(__name__)

# STATIC ITEMS
# Indian occupied Kashmir data
iok_bound = load_boundaries([6, 7])

# Pakistan centered Geo map
pak_bound = load_boundaries()

# Pakistan polygon
pak_polygon = load_polygon()

# Plotting Stuff
# Plotting IoK bounds
data0 = go.Scattermapbox(
    mode="lines",
    lat=[x[1] for x in iok_bound],
    lon=[x[0] for x in iok_bound],
    marker={'size': 20, 'color': "black"},
    text="IOK",
    hoverinfo="text")

# Plotting Pakistan bounds
data1 = go.Scattermapbox(
    mode="lines",
    lat=[x[1] for x in pak_bound],
    lon=[x[0] for x in pak_bound],
    marker={'size': 20, 'color': "green"},
    text="PAK IB",
    hoverinfo="text"
)

# Placeholder for tracks animation
data2 = go.Scattermapbox(lat=[None],
                         lon=[None],
                         mode='markers',
                         marker={'size': 5, 'color': "red"},
                         name='targets'
                         )

# Display detected GBADS (themselves) that have targets in their max range envelope. Depending on results, assign
# appropriate color and if needed draw a load out circle with different fill-color and border color and their opacities.
color = 'blue'
data3 = go.Scattermapbox(
    mode="markers",
    lat=[None],
    lon=[None],
    marker=go.scattermapbox.Marker(
        size=8,
        color=color
    ),
    text=[None],
    hoverinfo="text",
)

# Draw detected GBADS having enemy targets within their ranges as dynamic circles
data4 = go.Scattermapbox(
    mode="lines",
    fill="toself",
    fillcolor='rgba(0, 0, 255, 0.1)',  # Opacity of fill color via alpha channel
    lat=[None],  # lower x1, x2 and upper x4, x3
    lon=[None],  # lower y1, y2, and upper y4, y3
    marker={'size': 8, 'color': 'rgba(0, 0, 255, 0.5)', }  # Opacity of border color via alpha channel
)

# Draw max ranges of all enemy targets as an individual circle
data5 = go.Scattermapbox(
    mode="lines",
    fill="toself",
    fillcolor='rgba(255, 0, 0, 0.1)',  # Opacity of fill color via alpha channel
    lat=[None],  # lower x1, x2 and upper x4, x3
    lon=[None],  # lower y1, y2, and upper y4, y3
    marker={'size': 8, 'color': 'rgba(255, 0, 0, 0.2)', }  # Opacity of border color via alpha channel
)

# Plotting vp points in a single trace
color = 'pink'
data6 = go.Scattermapbox(
    mode="markers",
    lat=[None],
    lon=[None],
    marker=go.scattermapbox.Marker(
        # size=[point.size for point in vp_points],
        color=color
    ),
    text=[None],
    hoverinfo="text",
)

# Draw combine range of all enemy targets as a circle
data7 = go.Scattermapbox(
    # mode="lines+text",        # Seems like click, and drag and select is not working with text mode for us.
    mode="lines",
    textposition='top right',
    fillcolor='rgba(255, 0, 0, 0.1)',  # Opacity of fill color via alpha channel
    lat=[None],
    lon=[None],
    text=[None],
    marker={'size': 8, 'color': 'rgba(255, 0, 0, 0.5)', }  # Opacity of border color via alpha channel
)

# Draw straight line between VPs that are in range of enemy targets
data8 = go.Scattermapbox(
    mode="lines",
    textposition='top left',
    fillcolor='rgba(255, 255, 0, 0.1)',  # Opacity of fill color via alpha channel
    lat=[None],
    lon=[None],
    text=[None],
    marker={'size': 8, 'color': 'rgba(255, 255, 0, 0.5)', }  # Opacity of border color via alpha channel
)

# Draw straight line between VPs that will come in range of enemy targets soon enough
data9 = go.Scattermapbox(
    mode="lines",
    # fillcolor='rgba(255, 0, 255, 0.1)',  # Opacity of fill color via alpha channel
    lat=None,
    lon=None,
    # hoverinfo='skip',
    marker={'size': 8, 'color': 'rgba(255, 255, 255, 0.8)', }  # Opacity of border color via alpha channel
)

# Draw range of extended all enemy targets in polygon format
data10 = go.Scattermapbox(
    mode="lines",
    fill="toself",
    fillcolor='rgba(255, 0, 255, 0.01)',  # Opacity of fill color via alpha channel
    lat=None,  # lower x1, x2 and upper x4, x3
    lon=None,  # lower y1, y2, and upper y4, y3
    hoverinfo='skip',
    marker={'size': 8, 'color': 'rgba(255, 0, 255, 0.3)', }  # Opacity of border color via alpha channel
)

data = [data0, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10]

layout = {
    'mapbox': {'center': {'lat': 29.5, 'lon': 74},
               'layers': [{'below': 'traces',
                           'source': [
                               "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer"
                               "/tile/{z}/{y}/{x}"],
                           'sourceattribution': 'United States Geological Survey',
                           'sourcetype': 'raster'}],
               'style': 'carto-darkmatter',
               # 'style': 'white-bg',
               'zoom': 5.2},
    'showlegend': False,
    # 'template': '...'
}

target_data = pd.read_csv("C:/Users/DTEAIAPPS/PycharmProjects/flight-tracking/data/enemy/enemy-airborne/tracks.csv")

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']},
                      children=[
                          html.H1(children='Hello Dash', style={'textAlign': 'center', 'color': colors['text']}),
                          html.Div(children='Dash: A web application framework for your data.',
                                   style={'textAlign': 'center', 'color': colors['text']}),
                          dcc.Graph(id='live-update-graph', figure=go.Figure(data=data, layout=layout),
                                    style={'width': '100vw', 'height': '90vh'}),
                          dcc.Interval(id='control-interval', interval=1 * 1000, n_intervals=0,
                                       max_intervals=1),
                          dcc.Interval(id='interval-component', interval=2 * 1000, n_intervals=0,
                                       max_intervals=len(target_data) - 1)  # len(target_data)-1
                      ]
                      )


# @app.callback(
#     Output("interval-component", "interval"),
#     [Input("control-interval", "interval")]
# )
# def update_interval(interval):
#     return 2 * 1000

def udp_try(n_intervals):
    data_send = "Hello from the UDP client: " + str(n_intervals)
    data_send = str.encode(data_send)

    # Creating UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Binding Port
    server_address = ("localhost", 9999)
    # sock.bind(server_address)

    # time.sleep(0.01)
    # Request to the server
    sock.sendto(data_send, server_address)

    # Receiving from the server
    rec_data = sock.recvfrom(10*4096)
    json_obj = pickle.loads(rec_data[0])
    print(json_obj)
    return json_obj


@app.callback(Output('live-update-graph', 'figure'),
              # Output('live-update-graph', 'extendData'),
              [Input('interval-component', 'n_intervals')],
              [State('live-update-graph', 'figure')],
              prevent_initial_call=True
              )
def update_graph_live(n_intervals, existing):

    figure = udp_try(n_intervals)

    try:
        # figure = iterate()
        # Get updated info from tracks
        target = figure['target']
        print(n_intervals)

        # Plot all enemy targets detected via tracks
        existing['data'][2]['lat'] = [x.lat for x in target]
        existing['data'][2]['lon'] = [x.lon for x in target]
        existing['data'][2]['text'] = [x.name for x in target]
        existing['data'][2]['hoverinfo'] = ['text' for _ in range(len(target))]

        # # Plot max_ranges of all enemy air targets individually.
        # max_range_enemy_air_targets = figure['max_range_enemy_air_targets']
        # existing['data'][5]['lat'] = [x[1] for x in max_range_enemy_air_targets]
        # existing['data'][5]['lon'] = [x[0] for x in max_range_enemy_air_targets]
        # existing['data'][5]['hoverinfo'] = 'skip'

        # Get coordinates of the unified maximum single range of all enemy targets
        combine_polygon_exterior = figure["combine_polygon_exterior"]
        # Plot combine range of enemy targets
        existing['data'][7]['lat'] = [x[1] for x in combine_polygon_exterior]
        existing['data'][7]['lon'] = [x[0] for x in combine_polygon_exterior]
        existing['data'][7]['text'] = ['Combine Range' for _ in range(len(combine_polygon_exterior))]
        existing['data'][7]['hoverinfo'] = "text"

        # Combine range of extended all enemy targets in polygon format
        extended_combine_polygon_exterior = figure["extended_combine_polygon_exterior"]
        # Plot extended combine range of enemy targets
        existing['data'][10]['lat'] = [x[1] for x in extended_combine_polygon_exterior]
        existing['data'][10]['lon'] = [x[0] for x in extended_combine_polygon_exterior]
        existing['data'][10]['text'] = ['Area to hit next' for _ in range(len(extended_combine_polygon_exterior))]
        existing['data'][10]['hoverinfo'] = "text"

        vps = figure["vps"]
        if vps:
            # If VPs are within range of enemy target plot those VPs
            existing['data'][6]['lat'] = [x.lat for x in vps]
            existing['data'][6]['lon'] = [x.lon for x in vps]
            existing['data'][6]['text'] = [x.name for x in vps]
            existing['data'][6]['marker']['size'] = [x.size for x in vps]

            pairing_lines = figure["pairing_lines"]
            # Draw straight lines between VPS and closest enveloping enemy targets
            existing['data'][8]['lat'] = [x[0] for x in pairing_lines]
            existing['data'][8]['lon'] = [x[1] for x in pairing_lines]
            # existing['data'][8]['text'] = ['Combine Range' for _ in range(len(combine_polygon))]
            existing['data'][8]['hoverinfo'] = 'skip'

            gbads = figure["gbads"]
            if gbads:
                # Display detected GBADS (themselves) that have targets in their max range envelope
                existing['data'][3]['lat'] = [x.lat for x in gbads]
                existing['data'][3]['lon'] = [x.lon for x in gbads]
                existing['data'][3]['text'] = [x.name for x in gbads]

                # Display detected GBADS max ranges (circles) that have targets in their envelope
                max_zone_gbads = figure["max_zone_gbads"]
                existing['data'][4]['lat'] = [x[1] for x in max_zone_gbads]
                existing['data'][4]['lon'] = [x[0] for x in max_zone_gbads]
                existing['data'][4]['text'] = [x.name for x in gbads]
                # existing['data'][4]['hoverinfo'] = ['text' for x in range(len(gbads))]
                # existing['data'][4]['hoverinfo'] = 'skip'

        vps_next = figure["vps_next"]
        if vps_next:
            # Draw straight lines between VPS and closest enveloping extended enemy targets
            extended_pairing_lines = figure["extended_pairing_lines"]
            existing['data'][9]['lat'] = [x[0] for x in extended_pairing_lines]
            existing['data'][9]['lon'] = [x[1] for x in extended_pairing_lines]
            existing['data'][9]['text'] = "[x.name for x in vps_next]"
            existing['data'][9]['hoverinfo'] = "text"

        else:
            # Clear straight lines between VPS and closest enveloping extended enemy targets
            existing['data'][9]['lat'] = [None]
            existing['data'][9]['lon'] = [None]
            # existing['data'][8]['text'] = ['Combine Range' for _ in range(len(combine_polygon))]
            # existing['data'][9]['hoverinfo'] = 'skip'

    except StopIteration:
        print("Tracks list exhausted")

    return existing


@app.callback(
    Output('control-interval', 'interval'),
    Input('live-update-graph', 'selectedData'),
    Input('live-update-graph', 'clickData'),
    prevent_initial_call=True
)
def display_selected_data(selected_data, click_data):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] == 'live-update-graph.clickData':
        print("Click Data--->")
        print(click_data)

    else:
        print("Selected Data--->")
        print(selected_data.values())

    interval = 0
    return interval


if __name__ == "__main__":
    app.run_server(debug=True)
