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
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

backgroundCSS = f"""
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

st.markdown(f"<style>{backgroundCSS}{other_css}</style>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "General", "Season 1", "Season 2", "Season 3", "Season 4", "Season 5", "Season 6", "Season 7", "Season 8"
])

with tab1:

    total_episodios = episodes.shape[0]

    ratings_por_temp = episodes.groupby("Season")["Imdb rating"].mean()
    mejor_temp = ratings_por_temp.idxmax()
    mejor_rating = round(ratings_por_temp.max(), 2)

    views_por_temp = episodes.groupby("Season")["U.S. viewers(millions)"].mean()
    temp_mas_vista = views_por_temp.idxmax()
    vistas_max = round(views_por_temp.max(), 2)

    ubicacion_top = deaths["Location"].value_counts().idxmax()
    muertes_ubicacion = deaths["Location"].value_counts().max()

    mas_letal = deaths["Killer"].value_counts().idxmax()
    muertes_letal = deaths["Killer"].value_counts().max()

    total_muertes = deaths.shape[0]

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with st.container():
        st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        with col1:
            st.metric("Total de episodios", total_episodios)
        with col2:
            st.metric(f"Temporada mejor calificada", f"T{mejor_temp}", f"{mejor_rating} IMDB")
        with col3:
            st.metric(f"Temporada más vista", f"T{temp_mas_vista}", f"{vistas_max}M de vistas")
        with col4:
            st.metric("Ubicación con más muertes", ubicacion_top, f"{muertes_ubicacion} muertes")
        with col5:
            st.metric("Personaje más letal", mas_letal, f"{muertes_letal} muertes")
        with col6:
            st.metric("Total de muertes", total_muertes)
        st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("US viewers per Season")
    viewsGrouped = episodes.groupby("Season")["U.S. viewers(millions)"].mean().reset_index()
    viewsGrouped.columns = ["Season", "Average U.S. viewers (millions)"]
    fig = px.line(viewsGrouped, x="Season", y="Average U.S. viewers (millions)", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Imdb rating per Season")
    viewsGrouped = episodes.groupby("Season")["Imdb rating"].mean().reset_index()
    viewsGrouped.columns = ["Season", "Imdb rating"]
    fig = px.line(viewsGrouped, x="Season", y="Imdb rating", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Important deaths per Season")
    filtered_deaths = deaths[deaths["Importance"].between(2, 4)]
    deaths_grouped = (
        filtered_deaths
        .groupby(["Season", "Importance"])
        .size()
        .reset_index(name="Count")
    )
    fig = px.bar(
        deaths_grouped,
        x="Season",
        y="Count",
        color="Importance", 
        color_discrete_sequence=px.colors.sequential.Reds[::-1]  
    )
    fig.update_layout(barmode="stack")
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
