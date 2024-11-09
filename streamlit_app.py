import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim

# Geolocator to get the latitude and longitude of each country
geolocator = Nominatim(user_agent="emission_map")

def get_location(country):
    location = geolocator.geocode(country)
    if location:
        return location.latitude, location.longitude
    return None, None

# Streamlit app layout
st.title('Carbon Emission Visualization')

# File upload section
uploaded_file = st.file_uploader("Upload your emission data file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read the file (handle CSV or Excel files)
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith("xlsx"):
        df = pd.read_excel(uploaded_file)
    
    # Check if the file has the required columns
    if 'country' not in df.columns or 'date' not in df.columns or 'emission_value' not in df.columns:
        st.error("The file must contain 'country', 'date', and 'emission_value' columns.")
    else:
        # Display the data table
        st.write("Emission Data", df)
        
        # Create the map
        m = folium.Map(location=[20,0], zoom_start=2)

        # Add markers for each country
        marker_cluster = MarkerCluster().add_to(m)

        for index, row in df.iterrows():
            lat, lon = get_location(row['country'])
            if lat and lon:
                folium.Marker(
                    location=[lat, lon],
                    popup=f"{row['country']} - {row['emission_value']} tons",
                    icon=folium.Icon(color='blue')
                ).add_to(marker_cluster)

        # Display the map
        st.write("Carbon Emission Map")
        st.components.v1.html(m._repr_html_(), height=500)

else:
    st.info("Please upload a CSV or Excel file to begin.")

