import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import folium.plugins as plugins

# Page setup
:contentReference[oaicite:1]{index=1}
:contentReference[oaicite:2]{index=2}
:contentReference[oaicite:3]{index=3}

# Sidebar controls
:contentReference[oaicite:4]{index=4}
:contentReference[oaicite:5]{index=5}
:contentReference[oaicite:6]{index=6}
:contentReference[oaicite:7]{index=7}
:contentReference[oaicite:8]{index=8}

# Initialize map
:contentReference[oaicite:9]{index=9}
:contentReference[oaicite:10]{index=10}
any_layers_loaded = False

# Wind layer
if show_wind:
    try:
        :contentReference[oaicite:11]{index=11}
        any_layers_loaded = True
    :contentReference[oaicite:12]{index=12}
        :contentReference[oaicite:13]{index=13}

# River layer
if show_water:
    try:
        m.add_geojson(
            :contentReference[oaicite:14]{index=14}
            :contentReference[oaicite:15]{index=15}
        )
        any_layers_loaded = True
    :contentReference[oaicite:16]{index=16}
        :contentReference[oaicite:17]{index=17}

# Soilscapes WMS layer (England & Wales)
if show_soil:
    try:
        m.add_wms(
            :contentReference[oaicite:18]{index=18}
            layer="0",
            :contentReference[oaicite:19]{index=19}
        )
        any_layers_loaded = True
    :contentReference[oaicite:20]{index=20}
        :contentReference[oaicite:21]{index=21}

# Mast trees upload & display
:contentReference[oaicite:22]{index=22}
mast_df = None
if uploaded_file:
    :contentReference[oaicite:23]{index=23}
    :contentReference[oaicite:24]{index=24}
else:
    try:
        :contentReference[oaicite:25]{index=25}
    except:
        :contentReference[oaicite:26]{index=26}

:contentReference[oaicite:27]{index=27}
    try:
        m.add_points_from_xy(
            :contentReference[oaicite:28]{index=28}
            :contentReference[oaicite:29]{index=29}
        )
        m.add_heatmap(
            data=mast_df,
            latitude="lat",
            longitude="lon",
            :contentReference[oaicite:30]{index=30}
        )
        any_layers_loaded = True
    :contentReference[oaicite:31]{index=31}
        :contentReference[oaicite:32]{index=32}

# Basemap and legend
:contentReference[oaicite:33]{index=33}
if any_layers_loaded:
    :contentReference[oaicite:34]{index=34}
        :contentReference[oaicite:35]{index=35}
        :contentReference[oaicite:36]{index=36}
        :contentReference[oaicite:37]{index=37}
        :contentReference[oaicite:38]{index=38}
    })

# Render
:contentReference[oaicite:39]{index=39}
