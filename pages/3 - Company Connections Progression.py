import streamlit as st
from utils import company_connections_progression
import duckdb

st.set_page_config(
    page_title="2. Company Linkedin Connections Progression",
    page_icon="📄",
    layout="wide"
)

st.title("Company Linkedin Connections Progression")

if "context_data" in st.session_state:
    context_data = st.session_state["context_data"]
    company_connections_progression(context_data)
#    st.write(comp_set)
else:
    st.warning("Carica un file nella pagina Home per accedere a questa sezione.")