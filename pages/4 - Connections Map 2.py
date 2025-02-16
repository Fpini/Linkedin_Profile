import streamlit as st
from utils import create_df_per_map2
import duckdb
import plotly.express as px

st.set_page_config(
    page_title="4. Linkedin Connections Map 2",
    page_icon="📄",
    layout="wide"
)

st.title("Linkedin Connections Map 2")

if "context_data" in st.session_state:
    context_data = st.session_state["context_data"]
    if "Location" in context_data.columns:
        df = create_df_per_map2(context_data)
        #df = df_per_map.groupby(["Company", "Location", "Latitude","Longitude"]).size().reset_index(name="Count")

        # Imposta il tuo access token Mapbox
        px.set_mapbox_access_token("pk.eyJ1IjoiZnBpbmkiLCJhIjoiY203N2ZzN3A5MDQ3czJqc2h2aHVmemU4bCJ9.Y51CADcs8wC70kIxfpI9XgOKEN")

        # Creare la mappa con Mapbox
        fig = px.scatter_mapbox(
            df, 
            lat="Latitude", 
            lon="Longitude", 
            color="Company",  # Colore diverso per ogni azienda
            size = "Count",
            zoom=5,  # Livello di zoom
            mapbox_style="carto-positron",
            hover_name="Company",
            hover_data=["Count", "Location", "Latitude","Longitude"]  # Stile della mappa
        )

        fig.update_layout(dragmode="pan", showlegend=False, uirevision="static", margin={"r": 0, "t": 0, "l": 0, "b": 0})

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f'''Il file corrente non ha i dati per la costruzione della mappa. 
                   Torna alla home e carica un file con i dati di geolocalizzazione''')
else:
    st.warning("Carica un file nella pagina Home per accedere a questa sezione.")