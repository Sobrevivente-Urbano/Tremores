import json, requests
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline
import plotly.graph_objects as go

all_eq_data = requests.get(
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_month.geojson"
).json()


fig = go.Figure()

# Extracting all the important key features.
all_eq_dicts = all_eq_data["features"]

# Extracting the magnitude and the locations.
mags, lons, lats, hover_texts = [], [], [], []
for eq_dict in all_eq_dicts:
    mag = eq_dict["properties"]["mag"]
    lon = eq_dict["geometry"]["coordinates"][0]
    lat = eq_dict["geometry"]["coordinates"][1]
    title = eq_dict["properties"]["title"]
    
    if(mag >= 5):
        mags.append(mag)
        lons.append(lon)
        lats.append(lat)
        hover_texts.append(title)

colors = ["#CC0000","#CE1620","#E34234","#CD5C5C","#FF0000", "#FF1C00", "#FF6961", "#F4C2C2", "#FFFAFA"]

# Map the earthquakes.
data = [
    {
        "type": "scattergeo",
        "lon": lons,
        "lat": lats,
        "text": hover_texts,
        "marker": {
            "size": mags,
            "sizeref": 0.02025,
            "symbol": "circle",
            "sizemode": "area",
            "color": mags,
            "colorscale": "Viridis",
            "reversescale": True,
            "colorbar": {"title": "Magnitude"},
        },
    }
]

my_layout = Layout(title="Global Earthquakes",margin={"l":0,"r":0,"t":0,"b":0})

fig = go.Figure({"data": data, "layout": my_layout})

fig.write_image("Global-Earthquakes.png", scale=3)

