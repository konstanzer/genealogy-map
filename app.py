# genealogy_map.py
from flask import Flask, render_template
import folium
from geopy.geocoders import Nominatim
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Initialize map centered on the world
    m = folium.Map(location=[0, 0], zoom_start=2)
    
    # Sample genealogy data (replace with your own)
    data = [
        {"name": "John Doe", "birth": "London", "year": 1800, "color": "red"},
        {"name": "Jane Doe", "birth": "New York", "year": 1820, "color": "blue"},
        {"name": "Sam Smith", "birth": "Sydney", "year": 1850, "color": "green"}
    ]
    
    # Geocode and add markers
    geolocator = Nominatim(user_agent="genealogy_map")
    for person in data:
        try:
            loc = geolocator.geocode(person["birth"])
            if loc:
                folium.CircleMarker(
                    [loc.latitude, loc.longitude],
                    radius=5,
                    color=person["color"],
                    fill=True,
                    fill_color=person["color"],
                    popup=f"{person['name']} ({person['year']})"
                ).add_to(m)
        except:
            pass  # Skip if geocoding fails
    
    # Render map in HTML template
    return render_template('index.html', map_html=m._repr_html_())

if __name__ == '__main__':
    # Render assigns a PORT env var; default to 10000 for local testing
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
