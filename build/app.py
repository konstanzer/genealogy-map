import folium
from geopy.geocoders import Nominatim
from IPython.display import display

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
    try:
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
    except Exception as e:
        print(f"Error geocoding {person['birth']}: {e}")

# Display the map in Colab
display(m)
