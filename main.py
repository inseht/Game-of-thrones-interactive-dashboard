import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
 
df = pd.read_csv("csv/starsTransformers.csv")

st.write("""
# Game of thrones
interactive dashboard
""")

fig, ax = plt.subplots()
ax.hist(df['estrellas'], bins=range(1, 7), edgecolor='black', align='left')
ax.set_xlabel('Estrellas')
ax.set_ylabel('Frecuencia')
ax.set_title('Distribución de Estrellas')
st.pyplot(fig)
