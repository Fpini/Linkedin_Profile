import streamlit as st
import pandas as pd
from utils import connections_per_company, positions_per_company
import plotly.express as px
from streamlit_plotly_events import plotly_events  # 🔥 Libreria per intercettare i click

# Funzioni per resettare i livelli
def reset_to_main():
    st.session_state.selected_company = None
    st.session_state.selected_position = None
    st.session_state.click_data = None
    st.rerun()

def reset_to_category():
    st.session_state.selected_position = None
    st.session_state.click_data = None
    st.rerun()


st.set_page_config(
    page_title="4. Linkedin Profile Drill Down",
    page_icon="📄",
    layout="wide"
)

# Inizializzazione di session_state se non esiste
if "selected_company" not in st.session_state:
    st.session_state.selected_company = None
if "selected_position" not in st.session_state:
    st.session_state.selected_position = None
if "click_data" not in st.session_state:
    st.session_state.click_data = None

st.title("Company Linkedin Profile Drill Down")

# Verifica che il file sia stato caricato
if "context_data" in st.session_state:
    context_data = st.session_state["context_data"]
    
    # Visualizza le connessioni per azienda
    pos_per_comp = positions_per_company(context_data)
    st.write("Positions per company:", pos_per_comp)


    if pos_per_comp is not None: 
        # 1️⃣ Livello Principale (Categorie - Aziende)

        fig = px.bar(
            pos_per_comp,
            x="company",
            y="pos_per_comp",
            title="Livello Principale - Aziende",
            color = "position",
            text_auto = True,
            barmode="stack"
        )

                # Personalizzazione del layout
        fig.update_layout(
            xaxis_title="company",
            yaxis_title="positions per company",
            modebar_add=["resetScale2d"],
            xaxis=dict(
                rangeslider=dict(visible=True)),
            template="plotly_white"  # Tema chiaro
        )
        # Mostra il grafico
        st.plotly_chart(fig)
        st.write("Clicca su un'azienda per vedere le posizioni disponibili.")
    else:
        st.write("con_per_comp = None")
else:
    st.warning("Carica un file nella pagina Home per accedere a questa sezione.")
