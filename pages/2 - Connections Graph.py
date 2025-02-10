import streamlit as st
from utils import visualizza_grafo, create_comp_subset
import duckdb

st.set_page_config(
    page_title="2. Linkedin Connections Graph",
    page_icon="📄",
    layout="wide"
)

st.title("Linkedin Connections Graph")

if "context_data" in st.session_state:
    context_data = st.session_state["context_data"]
    comp_set = create_comp_subset(context_data, n=10000)
    st.write(comp_set)
    comp_subset = create_comp_subset(context_data, n=80)
    visualizza_grafo(comp_subset)
else:
    st.warning("Carica un file nella pagina Home per accedere a questa sezione.")