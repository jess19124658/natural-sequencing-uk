import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import folium
import folium.plugins as plugins

st.set_page_config(layout="wide")
st.title("UK Rewilding Dashboard: Wind, Water, Forest & Mast Year Planning")

st.success("✔️ Imports successful")

# Sidebar layer toggles
st.sidebar.header("Layer Controls")
show_wind = st.sidebar.checkbox("Show Wind Corridors", True)
show_water = st.sidebar.checkbox("Show Hydrology", True)
show_mast = st.sidebar.checkbox("Show Mast Tree Zones", True)
show_forest = st.sidebar.checkbox("Show NFI Woodland (GB)", True)

# Map setup
st.subheader("UK Rewilding Map")
m = leafmap.Map(center=[54.5, -3], zoom=6)
any_layers_loaded = False
legend_labels = {}

# Wind Corridors
if show_wind:
    try:
        wind_data = leafmap.load_geojson("data/uk_wind_corridors.geojson")
        wind_layer = folium.FeatureGroup(name="Wind Corridors")
        for feature in wind_data["features"]:
            coords = feature["geometry"]["coordinates"]
            folium.PolyLine(coords, color="red", weight=2, tooltip="Wind Path").add_to(wind_layer)
        m.add_layer(wind_layer)
        legend_labels["Wind Corridor"] = "🌀"
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Could not load wind corridors: {e}")

# River Systems
if show_water:
    try:
        river_data = leafmap.load_geojson("data/uk_rivers.geojson")
        river_layer = folium.FeatureGroup(name="River Systems")
        for feature in river_data["features"]:
            coords = feature["geometry"]["coordinates"]
            folium.PolyLine(coords, color="blue", weight=2, tooltip="River Flow").add_to(river_layer)
        m.add_layer(river_layer)
        legend_labels["River Systems"] = "💧"
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Could not load river data: {e}")

# Mast Tree Zones
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
        if "value" not in mast_df.columns:
            mast_df["value"] = 1  # default value for heatmap

        m.add_points_from_xy(
            mast_df,
            x="lon", y="lat", layer_name="Mast Tree Zones",
            info_columns=[col for col in mast_df.columns if col not in ["lon", "lat"]],
            marker_cluster=True
        )

        m.add_heatmap(
            data=mast_df,
            latitude="lat",
            longitude="lon",
            value="value",
            layer_name="Mast Tree Density"
        )
        legend_labels["Mast Tree Zones"] = "🌳"
        any_layers_loaded = True

    except Exception as e:
        st.warning(f"⚠️ Error showing mast data: {e}")

# NFI Woodland Layer (GB)
if show_forest:
    try:
        m.add_geojson(
            "data/nfi_woodland_gb_2023.geojson",
            layer_name="NFI Woodland (GB 2023)"
        )
        legend_labels["NFI Woodland (GB)"] = "🌲"
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Could not load NFI Woodland (GB): {e}")

# Basemap and Legend
m.add_basemap("CartoDB.DarkMatter")

if any_layers_loaded:
    try:
        m.add_legend(
            title="UK Rewilding Layers",
            labels=legend_labels
        )
    except Exception as e:
        st.warning(f"⚠️ Could not generate legend: {e}")

m.to_streamlit(height=700)
