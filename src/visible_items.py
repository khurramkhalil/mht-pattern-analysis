"""
# Plotting GBADS (Ground Assets) inside Pakistan boundary. Depending on results, assign appropriate
# color and if needed draw a load out circle with different fill-color and border color and their opacities.

color = 'blue'
data2 = go.Scattermapbox(
    mode="markers",
    lat=[point.lat for point in ground_assets],
    lon=[point.lon for point in ground_assets],
    marker=go.scattermapbox.Marker(
        size=8,
        color=color
    ),
    text=[point.name for point in ground_assets],
    hoverinfo="text",
)

# Calculate dynamic range of the current weapon system (declared by range_ parameter) as a circle
dynamic_circle = [item for sublist in [x.get_range() for x in ground_assets] for item in sublist]

# Draw dynamic range as a circle
data3 = go.Scattermapbox(
    mode="lines",
    fill="toself",
    fillcolor='rgba(0, 0, 255, 0.1)',  # Opacity of fill color via alpha channel
    lat=[x[1] for x in dynamic_circle],  # lower x1, x2 and upper x4, x3
    lon=[x[0] for x in dynamic_circle],  # lower y1, y2, and upper y4, y3
    marker={'size': 8, 'color': 'rgba(0, 0, 255, 0.5)', }  # Opacity of border color via alpha channel
)

# Calculate dynamic range of the current weapon system (declared by range_ parameter) as a circle
kill_circle = [item for sublist in [kill.kill_zone for kill in ground_assets] for item in sublist]

# Draw dynamic range as a circle
data4 = go.Scattermapbox(
    mode="lines",
    fill="toself",
    fillcolor='rgba(255, 0, 0, 0.1)',  # Opacity of fill color via alpha channel
    lat=[x[1] for x in kill_circle],  # lower x1, x2 and upper x4, x3
    lon=[x[0] for x in kill_circle],  # lower y1, y2, and upper y4, y3
    marker={'size': 8, 'color': 'rgba(255, 0, 0, 0.2)', }  # Opacity of border color via alpha channel
)

# Plotting vp points in a single trace
color = 'yellow'
data5 = go.Scattermapbox(
    mode="markers",
    # marker_symbol="square",
    lat=[point.lat for point in vp_points],
    lon=[point.lon for point in vp_points],
    marker=go.scattermapbox.Marker(
        size=[point.size for point in vp_points],
        color=color
    ),
    text=[point.name for point in vp_points],
    hoverinfo="text",
)

"""