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

# File uploader for new mast tree CSVs
uploaded_file = st.sidebar.file_uploader("Upload Mast Tree CSV", type=["csv"])
mast_df = None

if uploaded_file is not None:
    try:
        mast_df = pd.read_csv(uploaded_file)
        st.success("✅ Custom mast tree data uploaded!")
    except Exception as e:
        st.warning(f"⚠️ Could not read uploaded CSV: {e}")
else:
    try:
        mast_df = pd.read_csv("data/uk_mast_trees.csv")
    except Exception as e:
        st.warning(f"⚠️ Could not load default mast trees: {e}")

# Map setup
st.subheader("UK Rewilding Map")
m = leafmap.Map(center=[54.5, -3], zoom=6)
any_layers_loaded = False
legend_labels = {}

if show_wind:
    try:
        m.add_geojson("data/uk_wind_corridors.geojson", layer_name="Wind Corridors")
        legend_labels["Wind Corridor"] = "red"
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Could not load wind corridors: {e}")

if show_water:
    try:
        m.add_geojson("data/uk_rivers.geojson", layer_name="River Systems")
        legend_labels["River Systems"] = "blue"
        any_layers_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Could not load river data: {e}")

if show_mast and mast_df is not None:
    try:
        # Add clustering layer
        m.add_points_from_xy(
            mast_df,
            x="lon", y="lat", layer_name="Mast Tree Zones",
            info_columns=[col for col in mast_df.columns if col not in ["lon", "lat"]],
            marker_cluster=True
        )
        legend_labels["Mast Tree Zones"] = "green"

        # Check for heatmap value column
        heatmap_value = "value" if "value" in mast_df.columns else None

        m.add_heatmap(
            data=mast_df,
            latitude="lat",
            longitude="lon",
            value=heatmap_value,
            layer_name="Mast Tree Density"
        )
        if heatmap_value:
            legend_labels["Mast Tree Density"] = "orange"

        any_layers_loaded = True

    except Exception as e:
        st.warning(f"⚠️ Error showing mast data: {e}")

# Optional WMS layer: Soilscapes
try:
    m.add_wms_layer(
        url="https://ags2.craig.fr/arcgis/services/Soilscapes/MapServer/WMSServer?",
        layers="0",
        name="Soilscapes (England)",
        format="image/png",
        transparent=True
    )
    legend_labels["Soilscapes"] = "brown"
    any_layers_loaded = True
except Exception as e:
    st.warning(f"⚠️ Could not load Soilscapes layer: {e}")

m.add_basemap("CartoDB.DarkMatter")

# Add legend only if valid and safe
if any_layers_loaded and legend_labels:
    try:
        m.add_legend(
            title="UK Rewilding Layers",
            labels={k: str(v) for k, v in legend_labels.items()}
        )
    except Exception as e:
        st.warning(f"⚠️ Could not render legend: {e}")

m.to_streamlit(height=700)
