# app.py
from flask import Flask, render_template
import folium
import json
import os

app = Flask(__name__)

# Load data from JSON file
with open("genealogy_data.json", "r") as f:
    genealogy_data = json.load(f)

@app.route('/')
def index():
    # Initialize map with a global center (adjust based on your data's focus)
    m = folium.Map(location=[40, -36], zoom_start=4)

    # Add markers to the map using coordinates
    for person in genealogy_data:
        # Skip if lat/lon are missing
        if not person["lat"] or not person["lon"]:
            continue
        
        # Full name
        full_name = f"{person['first_name']} {person['last_name']}".strip()
        
        # Handle unknown years with '?'
        birth_year = person["birth_year"] if person["birth_year"] != "Unknown" else "?"
        death_year = person["death_year"] if person["death_year"] != "Unknown" else "?"
        
        # Popup text: "Full Name (birth-death)"
        popup_text = f"{full_name} ({birth_year}-{death_year})"
        
        folium.CircleMarker(
            location=[person["lat"], person["lon"]],
            radius=5,
            color=person["color"],
            fill=True,
            fill_color=person["color"],
            popup=folium.Popup(popup_text, max_width=200)
        ).add_to(m)

    # Render map in HTML template
    return render_template('index.html', map_html=m._repr_html_())

if __name__ == '__main__':
    # Render assigns a PORT env var; default to 10000 for local testing
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
