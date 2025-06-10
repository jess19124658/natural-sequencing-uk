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
        m.add_geojson("data/uk_rivers.geojson", layer_name="River Systems")
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Could not load river data: {e}")

# File uploader for new mast tree CSVs
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

if show_mast and mast_df is not None:
    try:
        # Add clustering layer
        m.add_points_from_xy(
            mast_df,
            x="lon", y="lat", layer_name="Mast Tree Zones",
            info_columns=[col for col in mast_df.columns if col not in ["lon", "lat"]],
            marker_cluster=True
        )

        # Add optional heatmap using just lat/lon
        m.add_heatmap(
            data=mast_df,
            latitude="lat",
            longitude="lon",
            layer_name="Mast Tree Density",
            value=None
        )
        any_layers_loaded = True

    except Exception as e:
        st.warning(f"⚠️ Error showing mast data: {e}")

m.add_basemap("CartoDB.DarkMatter")

if any_layers_loaded:
    m.add_legend(title="UK Rewilding Layers", labels={
        "Wind Corridor": "red",
        "River Systems": "blue",
        "Mast Tree Zones": "green"
    })

m.to_streamlit(height=700)
