import streamlit as st
from utils import company_connections_progression
import duckdb
import plotly.express as px

st.set_page_config(
    page_title="2. Company Linkedin Connections Drill Down",
    page_icon="📄",
    layout="wide"
)

st.title("Company Linkedin Connections Drill Down")

if "context_data" in st.session_state:
    context_data = st.session_state["context_data"]
    # Creazione di un campo di input testuale
    # Creazione dello stato per gestire il trigger
    if "submit_triggered" not in st.session_state:
        st.session_state.submit_triggered = False
    user_input = st.text_input("Input text to select your connections' companies:", on_change=lambda: st.session_state.update(submit_triggered=True))
    # Quando l'utente preme il pulsante, si attiva lo stato di elaborazione
    if st.button("Go") or st.session_state.submit_triggered:
        if user_input:
            df = company_connections_progression(context_data, user_input)
                # Creiamo il grafico a barre con l'asse X=Anno-Mese, Y=Conteggio, Colore=Evento
            if df is not None:
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
                st.warning("No selected companies")    
        else:
            st.warning("Input text to select companies")

else:
    st.warning("Carica un file nella pagina Home per accedere a questa sezione.")