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
        fig = px.line(conn_prog_glb, x=conn_prog_glb.year_month, y="cumulative_count", title="Global Cumulative Growth")
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
                    x="year", 
                    y="monthly_count", 
                    title="📊 Monthly Connections Growth", 
                    color="month",  # Cambia colore per ogni barra
                    text_auto=True,barmode="stack")  # Mostra i valori sopra le barre
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
    conn_per_comp=conn_per_comp[conn_per_comp['con_per_comp']>2]
    # Creazione del grafico con colori personalizzati
    if conn_per_comp is not None:
        fig = px.bar(conn_per_comp, 
                    x="company", 
                    y="con_per_comp", 
                    title="📊 Companies with more than 2 connections", 
                    color="company",  # Cambia colore per ogni barra
                    text_auto=True)  # Mostra i valori sopra le barre

        # Personalizzazione del layout
        fig.update_layout(
            xaxis_title="company",
            yaxis_title="con_per_comp",
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
