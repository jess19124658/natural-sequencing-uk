import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import folium.plugins as plugins

st.set_page_config(layout="wide")
st.title("UK Rewilding Dashboard: Wind, Water & Mast Year Planning")
st.success("✔️ Imports successful")

# Sidebar controls
st.sidebar.header("Layer Controls")
show_wind = st.sidebar.checkbox("Show Wind Corridors", True)
show_water = st.sidebar.checkbox("Show Hydrology", True)
show_mast = st.sidebar.checkbox("Show Mast Tree Zones", True)

# Map setup
st.subheader("UK Rewilding Map")
m = leafmap.Map(center=[54.5, -3], zoom=6)
any_layers_loaded = False

# Wind corridors
if show_wind:
    try:
        m.add_geojson("data/uk_wind_corridors.geojson", layer_name="Wind Corridors")
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Could not load wind corridors: {e}")

# River systems
if show_water:
    try:
        m.add_geojson("data/uk_rivers.geojson", layer_name="River Systems")
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Could not load river data: {e}")

# Mast tree upload
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

# Mast tree visual layers
if show_mast and mast_df is not None:
    try:
        # Add clustered mast points
        m.add_points_from_xy(
            mast_df,
            x="lon", y="lat",
            layer_name="Mast Tree Zones",
            info_columns=[col for col in mast_df.columns if col not in ["lat", "lon"]],
            marker_cluster=True
        )

        # Add heatmap of mast density
        m.add_heatmap(
            data=mast_df,
            latitude="lat",
            longitude="lon",
            layer_name="Mast Tree Density"
        )
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Error showing mast data: {e}")

# Basemap
m.add_basemap("CartoDB.DarkMatter")

# Add legend only if something is loaded
if any_layers_loaded:
    m.add_legend(
        title="UK Rewilding Layers",
        labels={
            "Wind Corridor": "red",
            "River Systems": "blue",
            "Mast Tree Zones": "green"
        }
    )

# Render map
m.to_streamlit(height=700)
