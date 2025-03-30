# genealogy_map.py
from flask import Flask, render_template
import folium
from folium.plugins import MarkerCluster
import json
import os

app = Flask(__name__)

# Load restructured data
try:
    with open("restruct_data.json", "r") as f:
        genealogy_data = json.load(f)
except FileNotFoundError:
    genealogy_data = []
    print("Warning: restruct_data.json not found")

@app.route('/')
def index():
    # Initialize map
    m = folium.Map(location=[40, -36], zoom_start=4)
    marker_cluster = MarkerCluster(spiderfy_distance_multiplier=1.5).add_to(m)

    for person in genealogy_data:
        birth_place = person["birth_place"]
        death_place = person["death_place"]
        full_name = f"{person['first_name']} {person['last_name']}".strip()
        birth_year = person["birth_year"] if person["birth_year"] != "Unknown" else "?"
        death_year = person["death_year"] if person["death_year"] != "Unknown" else "?"

        # Birth marker if coordinates available
        if birth_place["lat"] and birth_place["lon"]:
            folium.CircleMarker(
                location=[birth_place["lat"], birth_place["lon"]],
                radius=5,
                color=person["color"],
                fill=True,
                fill_color=person["color"],
                popup=folium.Popup(f"{full_name} ({birth_year})", max_width=200)
            ).add_to(marker_cluster)

        # Death marker if coordinates available
        if death_place["lat"] and death_place["lon"]:
            folium.CircleMarker(
                location=[death_place["lat"], death_place["lon"]],
                radius=5,
                color=person["color"],
                fill=True,
                fill_color=person["color"],
                popup=folium.Popup(f"{full_name} ({death_year})", max_width=200)
            ).add_to(marker_cluster)

        # Connect birth and death with dotted line if different coordinates
        if (birth_place["lat"] and birth_place["lon"] and 
            death_place["lat"] and death_place["lon"] and
            (birth_place["lat"] != death_place["lat"] or 
             birth_place["lon"] != death_place["lon"])):
            folium.PolyLine(
                locations=[
                    [birth_place["lat"], birth_place["lon"]],
                    [death_place["lat"], death_place["lon"]]
                ],
                color=person["color"],
                weight=2,
                dash_array="5, 5"  # Dotted line
            ).add_to(m)

    return render_template('index.html', map_html=m._repr_html_())
