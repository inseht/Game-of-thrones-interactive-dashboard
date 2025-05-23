import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("csv/starsTransformers.csv")

st.write("""
# Game of Thrones  
Interactive dashboard
""")

fig, ax = plt.subplots()

ax.hist(df['estrellas'], bins=range(1, 7), edgecolor='black', align='left', color='#8B4513')
ax.set_xlabel('Estrellas')
ax.set_ylabel('Frecuencia')
ax.set_title('Distribución de Estrellas')

fig.patch.set_alpha(0)
ax.patch.set_alpha(0)

st.pyplot(fig)
