import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Leer los CSV
data = pd.read_csv('csv/data.csv')
estrellas = pd.read_csv('csv/starsTransformers.csv')

st.title("Game of Thrones - Interactive Dashboard")

# Mostrar tabla con datos de data.csv
st.subheader("Datos de data.csv")
st.dataframe(data)

# Si 'estrellas' existe en starsTransformers.csv hacemos los gráficos
if 'estrellas' in estrellas.columns:
    min_estrellas = int(estrellas['estrellas'].min())
    max_estrellas = int(estrellas['estrellas'].max())

    estrellas_range = st.slider(
        "Selecciona el rango de estrellas",
        min_value=min_estrellas,
        max_value=max_estrellas,
        value=(min_estrellas, max_estrellas),
        step=1
    )

    df_filtrado = estrellas[(estrellas['estrellas'] >= estrellas_range[0]) & (estrellas['estrellas'] <= estrellas_range[1])]

    tipo_grafico = st.selectbox("Tipo de gráfico", ["Gráfico de pastel", "Gráfico de barras"])

    fig, ax = plt.subplots()

    conteo = df_filtrado['estrellas'].value_counts().sort_index()

    if tipo_grafico == "Gráfico de pastel":
        ax.pie(conteo.values, labels=conteo.index, autopct='%1.1f%%', colors=plt.cm.Oranges_r(range(len(conteo))))
        ax.set_title('Distribución de Estrellas (Pastel)')
    else:
        ax.bar(conteo.index, conteo.values, color='#8B4513', edgecolor='white')
        ax.set_title('Distribución de Estrellas (Barras)')
        ax.set_xlabel('Estrellas')
        ax.set_ylabel('Frecuencia')

    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    st.pyplot(fig)
else:
    st.warning("La columna 'estrellas' no existe en el CSV de estrellas.")
