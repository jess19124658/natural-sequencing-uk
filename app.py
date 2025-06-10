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
show_soil = st.sidebar.checkbox("Show Soilscapes", True)

# Map setup
st.subheader("UK Rewilding Map")
m = leafmap.Map(center=[54.5, -3], zoom=6)

any_layers_loaded = False

# Wind Corridors Layer
if show_wind:
    try:
        m.add_geojson("data/uk_wind_corridors.geojson", layer_name="Wind Corridors")
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Could not load wind corridors: {e}")

# River Systems Layer
if show_water:
    try:
        m.add_geojson("data/uk_rivers.geojson", layer_name="River Systems")
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Could not load river data: {e}")

# File uploader for community CSVs
uploaded_file = st.sidebar.file_uploader("Upload Mast Tree CSV", type=["csv"])
mast_df = None

if uploaded_file is not None:
    mast_df = pd.read_csv(uploaded_file)
    st.success("✅ Custom mast tree data uploaded!")
else:
    try:
        mast_df = pd.read_csv("data/uk_mast_trees.csv")
    except Exception as e:
        st.warning(f"⚠️ Could not load default mast trees: {e}")

# Mast Tree Data + Clustering + Heatmap
if show_mast and mast_df is not None:
    try:
        m.add_points_from_xy(
            mast_df,
            x="lon", y="lat",
            layer_name="Mast Tree Zones",
            info_columns=[col for col in mast_df.columns if col not in ["lon", "lat"]],
            marker_cluster=True
        )
        m.add_heatmap(
            data=mast_df,
            latitude="lat",
            longitude="lon",
            layer_name="Mast Tree Density"
        )
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Error showing mast data: {e}")

# Soilscapes WMS tile layer
if show_soil:
    try:
        m.add_wms_layer(
            url="https://ogc.bgs.ac.uk/cgi-bin/BGS_Bedrock_and_Superficial_Geology/wms",
            layers="Soilscapes",
            name="Soilscapes (Soil Types)",
            format="image/png",
            transparent=True,
            attribution="© Cranfield University/NERC"
        )
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Could not load Soilscapes WMS layer: {e}")

# Basemap and legend
m.add_basemap("CartoDB.DarkMatter")

if any_layers_loaded:
    m.add_legend(
        title="UK Rewilding Layers",
        labels={
            "Wind Corridors": "red",
            "River Systems": "blue",
            "Mast Tree Zones": "green",
            "Soilscapes (Soil Types)": "brown"
        }
    )

# Render map
m.to_streamlit(height=700)
