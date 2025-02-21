import streamlit as st
from utils import upload_file, process_csv_file
import duckdb
import time
from PIL import Image



st.set_page_config(page_title="Home - Profilo Linkedin", page_icon="📄", layout="wide")
st.cache_data.clear() 



if "duckdb_conn" in st.session_state:
    del st.session_state["duckdb_conn"]

immagine = Image.open("a-high-quality-streamlit-application-hom_YAAA5HthTTiTa4Ze4j7hNw__ifsh2uiRhmYnWqNbwV6KQ.jpeg")
st.image(immagine, caption="", use_container_width=True)

# Inserisci il CSS personalizzato per impostare lo sfondo

file = upload_file()

if file:
    context_data = process_csv_file(file)
    if context_data is not None:
        if "Location" in context_data.columns:
            nuovo_ordine = ["Last Name", "First Name", "Company", "Position", "Connected On", "Location", "Latitude", "Longitude"]
        else:
            nuovo_ordine = ["Last Name", "First Name", "Company", "Position", "Connected On"]
        context_data = context_data[nuovo_ordine]
        st.session_state["context_data"] = context_data
        st.success("File caricato con successo!")
        # Carica l'immagine usando un percorso relativo (assicurati che il file "immagine.jpg" sia nella stessa cartella o in una sottocartella)

        
    else:
        st.error("Errore durante l'elaborazione del file.")
else:
    st.warning("Carica un file per iniziare.")
