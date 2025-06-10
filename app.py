import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")
st.title("UK Rewilding Dashboard: Wind, Water & Mast Year Planning")

try:
    st.success("✔️ Imports successful")

    # Add map and chart code here...

except Exception as e:
    st.error(f"🚨 Something went wrong: {e}")


# Placeholder for Streamlit dashboard (app.py)
# Sidebar layer toggles
st.sidebar.header("Layer Controls")
show_wind = st.sidebar.checkbox("Show Wind Corridors", True)
show_water = st.sidebar.checkbox("Show Hydrology", True)
show_mast = st.sidebar.checkbox("Show Mast Tree Zones", True)

# Map setup
st.subheader("UK Rewilding Map")
m = leafmap.Map(center=[54.5, -3], zoom=6)

if show_wind:
    m.add_geojson("data/uk_wind_corridors.geojson", layer_name="Wind Corridors")

if show_water:
    m.add_geojson("data/uk_rivers.geojson", layer_name="River Systems")

if show_mast:
    m.add_points_from_xy(
        "https://raw.githubusercontent.com/opengeos/data/main/uk_mast_trees.csv",
        x="lon", y="lat", layer_name="Mast Tree Zones"
    )

m.add_basemap("CartoDB.DarkMatter")
m.add_legend(title="UK Rewilding Layers", labels={
    "Wind Corridor": "red",
    "River Systems": "blue",
    "Mast Tree Zones": "green"
})
m.to_streamlit(height=700)
import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")
st.title("UK Rewilding Dashboard: Wind, Water & Mast Year Planning")

try:

    import pandas as pd
    import leafmap.foliumap as leafmap
    st.success("✔️ Imports successful")

    # your map code continues here...

except Exception as e:
    st.error(f"🚨 Something went wrong: {e}")# Placeholder for Streamlit dashboard (app.py)

    st.success("✔️ Imports successful")

    # Sidebar controls
    st.sidebar.header("Layer Controls")
    show_wind = st.sidebar.checkbox("Show Wind Corridors", True)
    show_water = st.sidebar.checkbox("Show Hydrology", True)
    show_mast = st.sidebar.checkbox("Show Mast Tree Zones", True)

    # Map
    st.subheader("UK Rewilding Map")
    m = leafmap.Map(center=[54.5, -3], zoom=6)

    if show_wind:
        m.add_geojson("data/uk_wind_corridors.geojson", layer_name="Wind Corridors")

    if show_water:
        m.add_geojson("data/uk_rivers.geojson", layer_name="River Systems")

    if show_mast:
        m.add_points_from_xy(
            "https://raw.githubusercontent.com/opengeos/data/main/uk_mast_trees.csv",
            x="lon", y="lat", layer_name="Mast Tree Zones"
        )

    m.add_basemap("CartoDB.DarkMatter")
    m.add_legend(title="UK Rewilding Layers", labels={
        "Wind Corridor": "red",
        "River Systems": "blue",
        "Mast Tree Zones": "green"
    })
    m.to_streamlit(height=700)

except Exception as e:
    st.error(f"🚨 Something went wrong: {e}")
>>>>>>> 6c6958e662b9a89f1058c631407684e8760fb022
