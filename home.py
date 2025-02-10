import streamlit as st
from utils import upload_file, process_csv_file
import duckdb
#import subprocess
import sys
import time

st.set_page_config(page_title="Home - Profilo Linkedin", page_icon="📄", layout="wide")

file = upload_file()

if file:
    context_data = process_csv_file(file)
    if context_data is not None:
        st.session_state["context_data"] = context_data
        st.success("File caricato con successo!")
    else:
        st.error("Errore durante l'elaborazione del file.")
else:
    st.warning("Carica un file per iniziare.")
