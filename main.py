import base64
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Game of thrones: interactive dashboard",
    page_icon="resources/icon.png",
    layout="wide", 
)

st.image("resources/title.png", use_container_width =True)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        img_bytes = f.read()
        encoded_string = base64.b64encode(img_bytes).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}"); /* Cambia 'jpeg' por 'png' si tu imagen es .png */
            background-size: 100% 100%; /* Asegura que la imagen cubra todo el fondo */
            background-position: center; /* Centra la imagen */
            background-repeat: no-repeat; /* Evita que la imagen se repita */
            background-attachment: fixed; /* Mantiene la imagen fija al hacer scroll */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("resources/background.png")

episodes = pd.read_csv('csv/GOTepisodes.csv')
deaths = pd.read_csv('csv/GOTdeaths.csv')
stars = pd.read_csv('csv/starsTransformers.csv')

episodes['Season'] = pd.to_numeric(episodes['Season'], errors='coerce')
deaths['Season'] = pd.to_numeric(deaths['Season'], errors='coerce')

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "General", "Season 1", "Season 2", "Season 3", "Season 4", "Season 5", "Season 6", "Season 7", "Season 8"
])

with tab1:
    st.subheader("Datos de Muertes (Todos)")
    st.dataframe(deaths, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        min_stars = int(stars['stars'].min())
        max_stars = int(stars['stars'].max())

        stars_range = st.slider(
            "Selecciona el rango de stars",
            min_value=min_stars,
            max_value=max_stars,
            value=(min_stars, max_stars),
            step=1
        )

        df_filtrado = stars[
            (stars['stars'] >= stars_range[0]) & 
            (stars['stars'] <= stars_range[1])
        ]

        tipo_grafico = st.selectbox("Tipo de gráfico", ["Gráfico de pastel", "Gráfico de barras"])

    with col2:
        fig, ax = plt.subplots()
        conteo = df_filtrado['stars'].value_counts().sort_index()

        if tipo_grafico == "Gráfico de pastel":
            ax.pie(conteo.values, labels=conteo.index, autopct='%1.1f%%', colors=plt.cm.Oranges_r(range(len(conteo))))
            ax.set_title('Distribución de stars (Pastel)')
        else:
            ax.bar(conteo.index, conteo.values, color='#8B4513', edgecolor='white')
            ax.set_title('Distribución de stars (Barras)')
            ax.set_xlabel('stars')
            ax.set_ylabel('Frecuencia')

        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
        st.pyplot(fig)

tabs = [tab3, tab4, tab5, tab6, tab7, tab8, tab9]

for i, tab in enumerate(tabs):
    season = i + 2  
    with tab:
        st.subheader(f"Temporada {season}")
        
        muertes_temp = deaths[deaths['Season'] == season]
        st.markdown("### Muertes")
        st.dataframe(muertes_temp, use_container_width=True)

        episodios_temp = episodes[episodes['Season'] == season]
        st.markdown("### Episodios")
        st.dataframe(episodios_temp, use_container_width=True)
