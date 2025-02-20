import streamlit as st
from utils import create_df_per_map
import duckdb
import plotly.express as px

st.set_page_config(
    page_title="3. Linkedin Connections Map",
    page_icon="📄",
    layout="wide"
)

st.title("Linkedin Connections Map")

if "context_data" in st.session_state:
    context_data = st.session_state["context_data"]
    if "Location" in context_data.columns:
        df_per_map = create_df_per_map(context_data)
        # Creare la mappa con Plotly
        fig = px.scatter_geo(
            df_per_map,
            lat="Latitude",
            lon="Longitude",
            color = "Company",
            size = "Count",
            title="Linkedin Connection Map",
            projection="natural earth"
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, showlegend=False)
        # Mostra il grafico
        st.plotly_chart(fig,use_container_width=True)
    else:
        st.warning(f'''Il file corrente non ha i dati per la costruzione della mappa. 
                   Torna alla home e carica un file con i dati di geolocalizzazione''')
else:
    st.warning("Carica un file nella pagina Home per accedere a questa sezione.")