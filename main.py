import base64
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from streamlit_star_rating import st_star_rating

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
            st.metric("Total de pisodios", total_episodios)
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

        background_color = "rgba(75, 49, 21, 0.65)"
        line_color = "rgb(255, 255, 255)"
        font_color = "white"
        custom_brown_scale = ["#8a5f2c", "#CB8B3E", "#F4BA76", "#ECC18E"]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### US viewers per Season")
            viewsGrouped = episodes.groupby("Season")["U.S. viewers(millions)"].mean().reset_index()
            viewsGrouped.columns = ["Season", "Average U.S. viewers (millions)"]
            fig = px.line(viewsGrouped, x="Season", y="Average U.S. viewers (millions)", markers=True)
            fig.update_traces(line=dict(color=line_color))
            fig.update_layout(
                plot_bgcolor=background_color,
                paper_bgcolor=background_color,
                font=dict(color=font_color),
                xaxis=dict(color=font_color),
                yaxis=dict(color=font_color),
            )
            st.plotly_chart(fig, use_container_width=True, key="general_us_viewers")

        with col2:
            st.markdown("#### IMDb rating per Season")
            ratingsGrouped = episodes.groupby("Season")["Imdb rating"].mean().reset_index()
            ratingsGrouped.columns = ["Season", "Imdb rating"]
            fig = px.line(ratingsGrouped, x="Season", y="Imdb rating", markers=True)
            fig.update_traces(line=dict(color=line_color))
            fig.update_layout(
                plot_bgcolor=background_color,
                paper_bgcolor=background_color,
                font=dict(color=font_color),
                xaxis=dict(color=font_color),
                yaxis=dict(color=font_color),
            )
            st.plotly_chart(fig, use_container_width=True, key="general_imdb_rating")

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("#### Important Deaths by Importance Level")
            filtered_deaths = deaths[deaths["Importance"].between(2, 4)]
            importance_counts = (
                filtered_deaths
                .groupby("Importance")
                .size()
                .reset_index(name="Count")
            )
            fig_pie = px.pie(
                importance_counts,
                names="Importance",
                values="Count",
                color="Importance",
                color_discrete_sequence=custom_brown_scale
            )
            fig_pie.update_traces(textinfo="percent+label")
            fig_pie.update_layout(
                plot_bgcolor=background_color,
                paper_bgcolor=background_color,
                font=dict(color=font_color),
            )
            st.plotly_chart(fig_pie, use_container_width=True, key="general_important_deaths_pie")

        with col4:
            st.markdown("#### Death Methods Importance")
            method_data_total = (
                deaths.groupby("Method Category")["Importance"]
                .sum()
                .reset_index()
            )
            fig_treemap_total = px.treemap(
                method_data_total,
                path=["Method Category"],
                values="Importance",
                color="Method Category",
                color_discrete_sequence=custom_brown_scale
            )
            fig_treemap_total.update_layout(
                plot_bgcolor=background_color,
                paper_bgcolor=background_color,
                font=dict(color=font_color),
            )
            st.plotly_chart(fig_treemap_total, use_container_width=True, key="general_death_methods_treemap")


        st.subheader("House Impact by Season: Victims and Killers")
        brown_scale = ["#8a5f2c", "#CB8B3E", "#F4BA76", "#ECC18E"]
        victim_data = (
            deaths.groupby(["Season", "Allegiance death"])["Importance"]
            .sum()
            .reset_index()
            .rename(columns={"Allegiance death": "House", "Importance": "Total Importance"})
        )
        victim_data["Role"] = "Victim"
        killer_data = (
            deaths.groupby(["Season", "Allegiance killer"])["Importance"]
            .sum()
            .reset_index()
            .rename(columns={"Allegiance killer": "House", "Importance": "Total Importance"})
        )
        killer_data["Role"] = "Killer"
        combined_data = pd.concat([victim_data, killer_data])
        combined_data = combined_data[combined_data["House"].notna()]
        fig = px.bar(
            combined_data,
            x="Season",
            y="Total Importance",
            color="House",
            facet_col="Role",
            barmode="stack",
            color_discrete_sequence=brown_scale,
        )
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_layout(
            plot_bgcolor=background_color,
            paper_bgcolor=background_color,
            font=dict(color=font_color),
            xaxis=dict(color=font_color),
            yaxis=dict(color=font_color),
            legend_title_text="House"
        )

        st.plotly_chart(fig, use_container_width=True, key="general_house_impact")


tabs = [tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9]

tabs = [tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9]

for i, tab in enumerate(tabs):
    season = i + 1
    with tab:
        season_episodes = episodes[episodes["Season"] == season]
        season_deaths = deaths[deaths["Season"] == season]
        total_episodios = season_episodes.shape[0]

        mejor_capitulo_idx = season_episodes["Imdb rating"].idxmax()
        mejor_capitulo = season_episodes.loc[mejor_capitulo_idx, "Episode"]
        mejor_rating = round(season_episodes.loc[mejor_capitulo_idx, "Imdb rating"], 2)


        capitulo_mas_visto_idx = season_episodes["U.S. viewers(millions)"].idxmax()
        capitulo_mas_visto = season_episodes.loc[capitulo_mas_visto_idx, "Episode"]
        vistas_max = round(season_episodes.loc[capitulo_mas_visto_idx, "U.S. viewers(millions)"], 2)

        rating_temporada_prom = round(season_episodes["Imdb rating"].mean(), 2)
        vistas_temporada_prom = round(season_episodes["U.S. viewers(millions)"].mean(), 2)

        if not season_deaths.empty:
            ubicacion_top = season_deaths["Location"].value_counts().idxmax()
            muertes_ubicacion = season_deaths["Location"].value_counts().max()

            mas_letal = season_deaths["Killer"].value_counts().idxmax()
            muertes_letal = season_deaths["Killer"].value_counts().max()

            total_muertes = season_deaths.shape[0]
        else:
            ubicacion_top = "N/A"
            muertes_ubicacion = 0
            mas_letal = "N/A"
            muertes_letal = 0
            total_muertes = 0

        st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        with col1:
            st.metric("Total de episodios", total_episodios)
        with col2:
            st.metric(f"Mejor capítulo IMDb", f"Episodio {mejor_capitulo}", f"{mejor_rating} IMDB")
        with col3:
            st.metric(f"Capítulo más visto", f"Episodio {capitulo_mas_visto}", f"{vistas_max}M de vistas")
        with col4:
            st.metric("Ubicación con más muertes", ubicacion_top, f"{muertes_ubicacion} muertes")
        with col5:
            st.metric("Personaje más letal", mas_letal, f"{muertes_letal} muertes")
        with col6:
            st.metric("Total de muertes", total_muertes)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col7, col8 = st.columns(2)
        with col7:
            st.metric(f"Promedio IMDb Temporada {season}", f"{rating_temporada_prom}")
        with col8:
            st.metric(f"Promedio vistas Temporada {season}", f"{vistas_temporada_prom}M")

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("#### Important Deaths by Importance Level")
            filtered_deaths = season_deaths[season_deaths["Importance"].between(2, 4)]
            importance_counts = (
                filtered_deaths
                .groupby("Importance")
                .size()
                .reset_index(name="Count")
            )
            if importance_counts.empty:
                st.write("No hay muertes importantes en esta temporada.")
            else:
                fig_pie = px.pie(
                    importance_counts,
                    names="Importance",
                    values="Count",
                    color="Importance",
                    color_discrete_sequence=custom_brown_scale
                )
                fig_pie.update_traces(textinfo="percent+label")
                fig_pie.update_layout(
                    plot_bgcolor=background_color,
                    paper_bgcolor=background_color,
                    font=dict(color=font_color),
                )
                st.plotly_chart(fig_pie, use_container_width=True, key=f"{season}_chart_name3_pie")

        with col4:
            st.markdown("#### Death Methods Importance")
            if season_deaths.empty:
                st.write("No hay datos de métodos de muerte en esta temporada.")
            else:
                method_data_total = (
                    season_deaths.groupby("Method Category")["Importance"]
                    .sum()
                    .reset_index()
                )
                fig_treemap_total = px.treemap(
                    method_data_total,
                    path=["Method Category"],
                    values="Importance",
                    color="Method Category",
                    color_discrete_sequence=custom_brown_scale
                )
                fig_treemap_total.update_layout(
                    plot_bgcolor=background_color,
                    paper_bgcolor=background_color,
                    font=dict(color=font_color),
                )
                st.plotly_chart(fig_treemap_total, use_container_width=True, key=f"{season}_chart_name4_treemap")

        st.subheader("House Impact by Season: Victims and Killers")
        brown_scale = ["#8a5f2c", "#CB8B3E", "#F4BA76", "#ECC18E"]

        victim_data = (
            season_deaths.groupby(["Season", "Allegiance death"])["Importance"]
            .sum()
            .reset_index()
            .rename(columns={"Allegiance death": "House", "Importance": "Total Importance"})
        )
        victim_data["Role"] = "Victim"

        killer_data = (
            season_deaths.groupby(["Season", "Allegiance killer"])["Importance"]
            .sum()
            .reset_index()
            .rename(columns={"Allegiance killer": "House", "Importance": "Total Importance"})
        )
        killer_data["Role"] = "Killer"

        combined_data = pd.concat([victim_data, killer_data])
        combined_data = combined_data[combined_data["House"].notna()]

        if combined_data.empty:
            st.write("No hay datos de impacto por casas en esta temporada.")
        else:
            fig = px.bar(
                combined_data,
                x="Season",
                y="Total Importance",
                color="House",
                facet_col="Role",
                barmode="stack",
                color_discrete_sequence=brown_scale,
            )
            fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
            fig.update_layout(
                plot_bgcolor=background_color,
                paper_bgcolor=background_color,
                font=dict(color=font_color),
                xaxis=dict(color=font_color),
                yaxis=dict(color=font_color),
                legend_title_text="House"
            )
            st.plotly_chart(fig, use_container_width=True, key=f"{season}_chart_name5_houseimpact")


            if season == 8:
                avg_stars = round(stars["stars"].mean(), 1)

                st_star_rating(
                    label="Valoración promedio:",
                    maxValue=5,
                    defaultValue=avg_stars,
                    key="avg_rating",
                    emoticons=True,
                    read_only=True,
                    customCSS="div {background-color: rgba(75, 49, 21, 0.65); padding: 10px; border-radius: 5px;}"
                )

                fig = px.histogram(
                    stars,
                    x="stars",
                    nbins=5,
                    labels={"stars": "Estrellas"},
                    title="Distribución de estrellas de valoración",
                    color="stars",  
                    color_discrete_sequence=custom_brown_scale
                )

                fig.update_layout(
                    plot_bgcolor=background_color,
                    paper_bgcolor=background_color,
                    font=dict(color=font_color),
                    title_font=dict(color=font_color),
                    xaxis=dict(color=font_color, linecolor=line_color, gridcolor=line_color),
                    yaxis=dict(color=font_color, linecolor=line_color, gridcolor=line_color),
                    legend_title_text="Estrellas"
                )

                st.plotly_chart(fig, use_container_width=True)
