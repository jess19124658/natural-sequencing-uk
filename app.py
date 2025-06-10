import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")
st.title("UK Rewilding Dashboard: Wind, Water & Mast Year Planning")

st.success("✔️ Imports successful")

try:
    # Sidebar layer toggles
    st.sidebar.header("Layer Controls")
    show_wind = st.sidebar.checkbox("Show Wind Corridors", True)
    show_water = st.sidebar.checkbox("Show Hydrology", True)
    show_mast = st.sidebar.checkbox("Show Mast Tree Zones", True)

    # Map setup
    st.subheader("UK Rewilding Map")
    m = leafmap.Map(center=[54.5, -3], zoom=6)

    if show_wind:
        try:
            m.add_geojson("data/uk_wind_corridors.geojson", layer_name="Wind Corridors")
        except Exception as e:
            st.warning(f"⚠️ Could not load wind corridors: {e}")

    if show_water:
        try:
            m.add_geojson("data/uk_rivers.geojson", layer_name="River Systems")
        except Exception as e:
            st.warning(f"⚠️ Could not load river data: {e}")

    if show_mast:
        try:
            m.add_points_from_xy(
                "data/uk_mast_trees.csv",
                x="lon", y="lat", layer_name="Mast Tree Zones"
            )
        except Exception as e:
            st.warning(f"⚠️ Could not load mast trees: {e}")

    m.add_basemap("CartoDB.DarkMatter")
    m.add_legend(title="UK Rewilding Layers", labels={
        "Wind Corridor": "red",
        "River Systems": "blue",
        "Mast Tree Zones": "green"
    })
    m.to_streamlit(height=700)

except Exception as e:
    st.error(f"🚨 Something went wrong: {e}")
