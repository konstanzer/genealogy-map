from flask import Flask, render_template
from data import data
import folium
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Initialize map with a global center (adjust based on your data's focus)
    m = folium.Map(location=[20, 0], zoom_start=2)
    
    # Add markers to the map using coordinates
    for person in data:
        folium.CircleMarker(
            location=[person["lat"], person["lon"]],
            radius=5,
            color=person["color"],
            fill=True,
            fill_color=person["color"],
            popup=f"{person['name']} ({person['year']})"
        ).add_to(m)
    
    # Render map in HTML template
    return render_template('index.html', map_html=m._repr_html_())

if __name__ == '__main__':
    # Render assigns a PORT env var; default to 10000 for local testing
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
