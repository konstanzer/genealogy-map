# genealogy_map.py
from flask import Flask, render_template
import folium
from folium.plugins import MarkerCluster
import json
import os

app = Flask(__name__)

# Load data from data.json
try:
    with open("data.json", "r") as f:
        genealogy_data = json.load(f)
except FileNotFoundError:
    genealogy_data = []
    print("Warning: data.json not found")

@app.route('/')
def index():
    # Initialize map
    m = folium.Map(location=[40, -40], zoom_start=4)
    marker_cluster = MarkerCluster(
        max_cluster_radius=40,
        disable_clustering_at_zoom=6,  # Stop clustering at zoom 6 (individual markers from 6+)
        spiderfy_on_max_zoom=False,    # No spiderfying at max zoom
        spiderfy_distance_multiplier=1.5
    ).add_to(m)

    # Group people by coordinates for popups and track offsets
    coord_groups = {}  # (lat, lon) -> {"color": str, "people": list, "offset_count": int}

    # First pass: Collect all people at each coordinate
    for person in genealogy_data:
        birth_place = person["birth_place"]
        death_place = person["death_place"]
        full_name = f"{person['first_name']} {person['last_name']}".strip()
        birth_year = person["birth_year"] if person["birth_year"] != "Unknown" else "?"
        death_year = person["death_year"] if person["death_year"] != "Unknown" else "?"

        same_place = (birth_place["lat"] and death_place["lat"] and
                      birth_place["lon"] and death_place["lon"] and
                      birth_place["lat"] == death_place["lat"] and
                      birth_place["lon"] == death_place["lon"])

        # Birth entry
        if birth_place["lat"] and birth_place["lon"]:
            coords = (birth_place["lat"], birth_place["lon"])
            if coords not in coord_groups:
                coord_groups[coords] = {"color": person["color"], "people": [], "offset_count": 0}
            entry = f"{full_name} ({birth_year}" + (f"-{death_year}" if same_place else "") + ")"
            if entry not in coord_groups[coords]["people"]:
                coord_groups[coords]["people"].append(entry)

        # Death entry if different
        if death_place["lat"] and death_place["lon"] and not same_place:
            coords = (death_place["lat"], death_place["lon"])
            if coords not in coord_groups:
                coord_groups[coords] = {"color": person["color"], "people": [], "offset_count": 0}
            entry = f"{full_name} (d.{death_year})"
            if entry not in coord_groups[coords]["people"]:
                coord_groups[coords]["people"].append(entry)

    # Second pass: Plot markers with offsets and lines
    for person in genealogy_data:
        birth_place = person["birth_place"]
        death_place = person["death_place"]
        full_name = f"{person['first_name']} {person['last_name']}".strip()
        birth_year = person["birth_year"] if person["birth_year"] != "Unknown" else "?"
        death_year = person["death_year"] if person["death_year"] != "Unknown" else "?"

        same_place = (birth_place["lat"] and death_place["lat"] and
                      birth_place["lon"] and death_place["lon"] and
                      birth_place["lat"] == death_place["lat"] and
                      birth_place["lon"] == death_place["lon"])

        # Birth marker with offset
        if birth_place["lat"] and birth_place["lon"]:
            birth_coords = (birth_place["lat"], birth_place["lon"])
            group = coord_groups[birth_coords]
            offset_count = group["offset_count"]
            birth_lat = birth_place["lat"] + (offset_count * 0.001)
            birth_lon = birth_place["lon"] + (offset_count * 0.001)
            group["offset_count"] += 1

            popup_text = "<br>".join(group["people"])
            folium.CircleMarker(
                location=[birth_lat, birth_lon],
                radius=5,
                color=group["color"],
                fill=True,
                fill_color=group["color"],
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(marker_cluster)

        # Death marker with offset if different
        if death_place["lat"] and death_place["lon"] and not same_place:
            death_coords = (death_place["lat"], death_place["lon"])
            group = coord_groups[death_coords]
            offset_count = group["offset_count"]
            death_lat = death_place["lat"] + (offset_count * 0.001)
            death_lon = death_place["lon"] + (offset_count * 0.001)
            group["offset_count"] += 1

            popup_text = "<br>".join(group["people"])
            folium.CircleMarker(
                location=[death_lat, death_lon],
                radius=5,
                color=group["color"],
                fill=True,
                fill_color=group["color"],
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(marker_cluster)

            # Connect with thinner, paler, dotted line
            folium.PolyLine(
                locations=[
                    [birth_lat, birth_lon],
                    [death_lat, death_lon]
                ],
                color=person["color"],
                weight=0.5,        # Thinner line
                opacity=0.5,       # Paler line
                dash_array="5, 5"  # Dotted
            ).add_to(m)

    return render_template('index.html', map_html=m._repr_html_())
