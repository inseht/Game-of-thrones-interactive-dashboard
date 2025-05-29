import base64
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

episodes = pd.read_csv('csv/GOTepisodes.csv')
deaths = pd.read_csv('csv/GOTdeaths.csv')
stars = pd.read_csv('csv/starsTransformers.csv')

st.set_page_config(
    page_title="Game of thrones: Interactive dashboard",
    page_icon="resources/images/icon.png",
    layout="wide", 
)

def get_encoded_bg(image_file):
    with open(image_file, "rb") as f:
        img_bytes = f.read()
        encoded_string = base64.b64encode(img_bytes).decode()
    return encoded_string

encoded_string = get_encoded_bg("resources/images/background.png")

def load_css(file_path):
    with open(file_path, "r") as f:
        return f.read()

background_css = f"""
.stApp {{
    background-image: url("data:image/png;base64,{encoded_string}");
    background-size: 100% 100%;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

overflow: hidden !important;
height: 100vh !important;
"""

other_css = load_css("resources/styles/styles.css")

st.markdown(f"<style>{background_css}{other_css}</style>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "General", "Season 1", "Season 2", "Season 3", "Season 4", "Season 5", "Season 6", "Season 7", "Season 8"
])

with tab1:
    st.subheader("US viewers per Season")
    viewsGrouped = episodes.groupby("Season")["U.S. viewers(millions)"].mean().reset_index()
    viewsGrouped.columns = ["Season", "Average U.S. viewers (millions)"]

    fig = px.line(viewsGrouped, x="Season", y="Average U.S. viewers (millions)", markers=True,
                  title="Average U.S. viewers by Season")
    st.plotly_chart(fig, use_container_width=True)


    st.subheader("Deaths per Season")

    important_deaths = deaths[deaths["Importance"] >= 2]
    deaths_count = important_deaths.groupby("Season").size().reset_index(name="Count")
    fig = px.bar(deaths_count, x="Season", y="Count",
                title="Important deaths (Importance ≥ 2) per Season")
    fig.update_yaxes(range=[10, deaths_count["Count"].max() + 5])
    st.plotly_chart(fig, use_container_width=True)



tabs = [tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9]

for i, tab in enumerate(tabs):
    season = i + 1  
    with tab:
        st.subheader(f"Temporada {season}")
        
        muertes_temp = deaths[deaths['Season'] == season]
        st.markdown("### Muertes")
        st.dataframe(muertes_temp, use_container_width=True)

        episodios_temp = episodes[episodes['Season'] == season]
        st.markdown("### Episodios")
        st.dataframe(episodios_temp, use_container_width=True)
