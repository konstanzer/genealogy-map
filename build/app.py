from flask import Flask, render_template
from geopy.geocoders import Nominatim
import folium

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

    # Geocode locations and add markers
    geolocator = Nominatim(user_agent="genealogy_map")
    for person in data:
        location = geolocator.geocode(person["birth"])
        if location:  # Check if geocoding worked
            folium.CircleMarker(
                location=[location.latitude, location.longitude],
                radius=5,
                color=person["color"],
                fill=True,
                fill_color=person["color"],
                popup=f"{person['name']} ({person['year']})"
            ).add_to(m)

    # Save map to a string to embed in HTML
    map_html = m._repr_html_()
    return render_template('index.html', map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
