import streamlit as st
from utils import (connections_per_company, connections_per_position, company_count, position_count,
                   connections_progression, connections_progression_global, max_conn_prog_glb)
import plotly.express as px

st.set_page_config(
    page_title="1. Linkedin Connections Overview",
    page_icon="📄",
    layout="wide"
)

st.title("Linkedin Connections Overview")

if "context_data" in st.session_state:
    context_data = st.session_state["context_data"]
#
#  Total connections' number
#     
    conn_prog_glb = connections_progression_global(context_data)
    total_connections = max_conn_prog_glb(conn_prog_glb)
    st.header(f'Total number of connections: {total_connections}')
#
#  Global period connections' trend
#     
    if conn_prog_glb is not None:
        conn_prog_glb["year_month"] = conn_prog_glb["year"].astype(str) + "-" + conn_prog_glb["month"].astype(str).str.zfill(2)
        # Creazione del grafico con Plotly
        fig = px.line(conn_prog_glb, x=conn_prog_glb.year_month, y="cumulative_count", title="Global Cumulative Progression")
        # Aggiunge il pulsante per resettare lo zoom
        fig.update_layout(modebar_add=["resetScale2d"])
        # Mostra il grafico in Streamlit
        st.plotly_chart(fig)
#
#  Monthly connections' growth
#     
    conn_prog = connections_progression(context_data)
    if conn_prog is not None:
        conn_prog["year_month"] = conn_prog["year"].astype(str) + "-" + conn_prog["month"].astype(str).str.zfill(2)
        # Creazione del grafico con colori personalizzati
        fig = px.bar(conn_prog, 
                    x="year_month", 
                    y="monthly_count", 
                    title="📊 Monthly Connections", 
                    color="year_month",  # Cambia colore per ogni barra
                    text_auto=True)  # Mostra i valori sopra le barre
        # Personalizzazione del layout
        fig.update_layout(
            xaxis_title="year_month",
            yaxis_title="monthly_count",
            modebar_add=["resetScale2d"],
            xaxis=dict(
                rangeslider=dict(visible=True)),
            template="plotly_white"  # Tema chiaro
        )
        # Mostra il grafico
        st.plotly_chart(fig)
#
#  Most connected Companies  
#
    company_count = company_count(context_data)
    st.header(f'Total number of connections companies: {company_count}')
#    value_comp = st.slider("Choose a value", min_value=1, max_value=company_count, value=10)
    conn_per_comp = connections_per_company(context_data)
    # Creazione del grafico con colori personalizzati
    if conn_per_comp is not None:
        fig = px.bar(conn_per_comp, 
                    x="Company", 
                    y="count_company", 
                    title="📊 Companies linked to more than 2 connections", 
                    color="Company",  # Cambia colore per ogni barra
                    text_auto=True)  # Mostra i valori sopra le barre

        # Personalizzazione del layout
        fig.update_layout(
            xaxis_title="Company",
            yaxis_title="count_company",
            modebar_add=["resetScale2d"],
            xaxis=dict(
                rangeslider=dict(visible=True)),
            template="plotly_white"  # Tema chiaro
        )
        # Mostra il grafico
        st.plotly_chart(fig)
#
#  Most popular connection's Positions  
#

    position_count = position_count(context_data)
    st.header(f'Total number of connections positions: {position_count}')

    conn_per_pos = connections_per_position(context_data)
    # Creazione del grafico con colori personalizzati
    if conn_per_pos is not None:
        fig = px.bar(conn_per_pos, 
                    x="Position", 
                    y="count_position", 
                    title="📊 Positions linked to more than 2 connections ", 
                    color="Position",  # Cambia colore per ogni barra
                    text_auto=True)  # Mostra i valori sopra le barre

        # Personalizzazione del layout
        fig.update_layout(
            xaxis_title="year_month",
            yaxis_title="monthly_count",
            modebar_add=["resetScale2d"],
            xaxis=dict(
                rangeslider=dict(visible=True)),
            template="plotly_white"  # Tema chiaro
        )
        # Mostra il grafico
        st.plotly_chart(fig)

else:
    st.warning("Carica un file nella pagina Home per accedere a questa sezione.")
