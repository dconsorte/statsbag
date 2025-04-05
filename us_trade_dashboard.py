# Streamlit Web Dashboard: U.S. Trade Realignment Impact by Industry

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import squarify

# Tile grid for all 50 states + DC
tile_grid = [
    ["WA", "MT", "ND", "SD", "MN", "WI", "MI", "NY", "VT", "NH", "ME"],
    ["OR", "ID", "WY", "NE", "IA", "IL", "IN", "OH", "PA", "MA", "CT"],
    ["CA", "NV", "UT", "CO", "MO", "KY", "WV", "VA", "NJ", "RI", "DE"],
    ["AZ", "NM", "OK", "KS", "AR", "TN", "NC", "SC", "DC", "MD", ""],
    ["HI", "AK", "TX", "LA", "MS", "AL", "GA", "FL", "", "", ""]
]

tiles = []
for row_idx, row in enumerate(tile_grid):
    for col_idx, state in enumerate(row):
        if state:
            tiles.append({"state": state, "row": row_idx, "col": col_idx})

tile_df = pd.DataFrame(tiles)

region_assignments = {
    "West Coast": ["CA", "OR", "WA", "NV", "AK", "HI"],
    "Midwest": ["IL", "IN", "IA", "OH", "WI", "MI", "MN", "MO", "ND", "SD", "NE", "KS"],
    "South": ["TX", "OK", "AR", "LA", "KY", "TN", "MS", "AL", "GA", "FL", "SC", "NC", "VA", "WV"],
    "Northeast": ["NY", "PA", "NJ", "MA", "CT", "RI", "VT", "NH", "ME", "DE", "MD", "DC"],
    "Rural Areas": ["MT", "ID", "UT", "CO", "NM", "AZ", "WY"]
}

state_to_region = {state: region for region, states in region_assignments.items() for state in states}

industry_impact_by_region = {
    "Tech": {"West Coast": -1, "Midwest": 0, "South": 0, "Northeast": 1, "Rural Areas": 0},
    "Agriculture": {"West Coast": -1, "Midwest": -1, "South": -1, "Northeast": 0, "Rural Areas": -2},
    "Manufacturing": {"West Coast": 1, "Midwest": 2, "South": 2, "Northeast": 1, "Rural Areas": 0},
    "Logistics": {"West Coast": 2, "Midwest": 1, "South": 2, "Northeast": 1, "Rural Areas": 1},
    "Energy": {"West Coast": 1, "Midwest": 1, "South": 2, "Northeast": 0, "Rural Areas": 2},
    "Construction": {"West Coast": 1, "Midwest": 1, "South": 2, "Northeast": 1, "Rural Areas": 1},
    "Healthcare": {"West Coast": 1, "Midwest": 1, "South": 1, "Northeast": 1, "Rural Areas": 1},
    "Aerospace": {"West Coast": -2, "Midwest": -1, "South": -1, "Northeast": -1, "Rural Areas": 0},
    "Retail": {"West Coast": -1, "Midwest": 0, "South": 0, "Northeast": 0, "Rural Areas": -1}
}

sample_gdp_data = {
    "Tech": {"CA": 800, "TX": 300, "NY": 250, "WA": 180, "MA": 150, "IL": 100, "GA": 80, "CO": 60, "NC": 70, "FL": 120},
    "Agriculture": {"CA": 50, "TX": 60, "IA": 45, "NE": 40, "IL": 55, "MN": 38, "KS": 42, "IN": 30, "WI": 25, "MO": 28},
    "Manufacturing": {"TX": 350, "CA": 300, "IL": 200, "MI": 180, "OH": 160, "IN": 150, "NC": 100, "PA": 90},
    "Logistics": {"TX": 280, "IL": 200, "GA": 160, "CA": 150, "TN": 140, "NY": 100, "FL": 100},
    "Energy": {"TX": 400, "ND": 80, "LA": 100, "OK": 90, "CA": 70, "PA": 60, "CO": 50},
    "Construction": {"TX": 250, "CA": 200, "FL": 180, "NY": 160, "IL": 120, "OH": 100},
    "Healthcare": {"CA": 350, "TX": 300, "NY": 250, "FL": 200, "PA": 150, "IL": 130, "OH": 120},
    "Aerospace": {"WA": 220, "CA": 200, "TX": 180, "MO": 140, "CT": 120},
    "Retail": {"CA": 300, "TX": 250, "FL": 200, "NY": 180, "IL": 160, "PA": 140}
}

def plot_tile_map_with_gdp(industry_name):
    impact_map = industry_impact_by_region[industry_name]
    gdp_data = sample_gdp_data[industry_name]
    fig, ax = plt.subplots(figsize=(10, 6))

    for _, row in tile_df.iterrows():
        state = row["state"]
        region = state_to_region.get(state, None)
        impact = impact_map.get(region, 0)
        color = plt.cm.RdYlGn((impact + 2) / 4)

        rect = plt.Rectangle((row["col"], -row["row"]), 1, -1, facecolor=color, edgecolor='black')
        ax.add_patch(rect)

        gdp = gdp_data.get(state, 0)
        if gdp > 0:
            bubble_size = np.sqrt(gdp) * 4
            ax.scatter(row["col"] + 0.5, -row["row"] - 0.5, s=bubble_size**2, color='black', alpha=0.2)
            ax.text(row["col"] + 0.5, -row["row"] - 0.5, state, ha='center', va='center', fontsize=8, color='white')
        else:
            ax.text(row["col"], -row["row"] - 1, state, fontsize=8)

    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-5.5, 0.5)
    ax.set_aspect('equal')
    ax.set_title(f"{industry_name} Industry: Impact & GDP", fontsize=14)
    ax.axis("off")
    st.pyplot(fig)

def plot_treemap_for_industry(industry_name):
    gdp_data = sample_gdp_data[industry_name]
    impact_map = industry_impact_by_region[industry_name]

    labels, sizes, colors = [], [], []
    for state, gdp in gdp_data.items():
        region = state_to_region.get(state, None)
        impact = impact_map.get(region, 0)
        label = f"{state}\n${gdp}B"
        labels.append(label)
        sizes.append(gdp)
        colors.append(plt.cm.RdYlGn((impact + 2) / 4))

    fig = plt.figure(figsize=(10, 6))
    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.8, text_kwargs={'fontsize': 10})
    plt.axis('off')
    plt.title(f"{industry_name} Industry: Treemap by GDP & Impact", fontsize=14)
    st.pyplot(fig)

# Streamlit App UI
st.title("U.S. Trade Realignment Impact Dashboard")
st.write("Visualize the economic impact of trade realignment by industry, showing both regional impact and GDP contribution.")
selected_industry = st.selectbox("Select Industry:", list(industry_impact_by_region.keys()))

plot_tile_map_with_gdp(selected_industry)
plot_treemap_for_industry(selected_industry)

# Add clickable link at bottom
st.markdown("---")
st.markdown("Built with ❤️ by [StatsBag](https://statsbag.com/)", unsafe_allow_html=True)