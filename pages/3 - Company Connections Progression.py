import streamlit as st
from utils import company_connections_progression
import duckdb
import plotly.express as px

st.set_page_config(
    page_title="2. Company Linkedin Connections Progression",
    page_icon="📄",
    layout="wide"
)

st.title("Company Linkedin Connections Progression")

if "context_data" in st.session_state:
    context_data = st.session_state["context_data"]
    df = company_connections_progression(context_data)
        # Creiamo il grafico a barre con l'asse X=Anno-Mese, Y=Conteggio, Colore=Evento
    fig = px.bar(df, 
             x='year_month', 
             y='monthly_count', 
             color='COMPANY', 
             title="Monthly Connections Count",
             labels={'year_month': 'Year-Month', 'count': 'Connections Number'},
             barmode='group')

    # Mostra il grafico
    st.plotly_chart(fig, key="company connections progression")
else:
    st.warning("Carica un file nella pagina Home per accedere a questa sezione.")