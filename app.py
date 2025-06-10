import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import folium.plugins as plugins

st.set_page_config(layout="wide")
st.title("UK Rewilding Dashboard: Wind, Water & Mast Year Planning")
st.success("✔️ Imports successful")

# Sidebar layer toggles
st.sidebar.header("Layer Controls")
show_wind = st.sidebar.checkbox("Show Wind Corridors", True)
show_water = st.sidebar.checkbox("Show Hydrology", True)
show_mast = st.sidebar.checkbox("Show Mast Tree Zones", True)

# Map setup
st.subheader("UK Rewilding Map")
m = leafmap.Map(center=[54.5, -3], zoom=6)
any_layers_loaded = False

if show_wind:
    try:
        m.add_geojson("data/uk_wind_corridors.geojson", layer_name="Wind Corridors")
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Could not load wind corridors: {e}")

if show_water:
    try:
        m.add_geojson(
            "https://raw.githubusercontent.com/jess19124658/natural-sequencing-uk/main/data/uk_os_open_rivers.geojson",
            layer_name="OS Open Rivers"
        )
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Could not load OS Open Rivers: {e}")

# (mast upload + heatmap/clustering code continues unchanged)

m.add_basemap("CartoDB.DarkMatter")
if any_layers_loaded:
    m.add_legend(title="UK Rewilding Layers", labels={
        "Wind Corridor": "red",
        "River Systems": "blue",
        "Mast Tree Zones": "green"
    })
m.to_streamlit(height=700)
