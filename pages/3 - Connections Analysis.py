import streamlit as st
from utils import company_connections_progression, company_advanced_search  # Assicurarsi che company_advanced_search esista in utils
import duckdb
import plotly.express as px

def on_comp_multiselect_change():
    st.write(change)
    run

st.set_page_config(
    page_title="5. Company Linkedin Connections Drill Down",
    page_icon="📄",
    layout="wide"
)

st.title("Company Linkedin Connections Drill Down")

if "context_data" in st.session_state:
    context_data = st.session_state["context_data"]
    
    # Creazione di due tab per le due modalità di ricerca
    tab1, tab2 = st.tabs(["Connections Drill Down", "Advanced Search"])
    
    # --- Tab 1: Ricerca Classica ---
    with tab1:
        with st.form("connections_search_form"):
            user_input = st.text_input("Inserisci il testo per selezionare le aziende delle tue connessioni:")
            submitted = st.form_submit_button("Go")
            
            if submitted:
                if user_input:
                    df = company_connections_progression(context_data, user_input)
                    if df is not None and not df.empty:
                        # Creazione del grafico a barre
                        fig = px.bar(
                            df, 
                            x='year_month', 
                            y='monthly_count', 
                            color='COMPANY', 
                            title="Monthly Connections Count",
                            labels={'year_month': 'Year-Month', 'monthly_count': 'Connections Number'},
                            barmode='group'
                        )
                        st.plotly_chart(fig, use_container_width=True, key="company_connections_progression")
                    else:
                        st.warning("Nessuna azienda corrisponde al criterio selezionato.")
                else:
                    st.warning("Inserisci un testo per selezionare le aziende.")
    
    # --- Tab 2: Ricerca Avanzata ---
    with tab2:
        with st.form("advanced_search_form"):
            option = st.radio(
                "Seleziona un'opzione:",
                ["Company", "Position"]
            )

            # Carica la lista unica delle aziende
            companies_list = sorted(context_data["Company"].dropna().unique().tolist())

            # Multiselect per selezionare le aziende (filtro principale)
            selected_companies = st.multiselect("Seleziona le aziende", companies_list)

            # Seleziona dinamicamente le posizioni in base alle aziende selezionate
            # if selected_companies:
            #     # Filtra il DataFrame in base alle aziende selezionate e prendi le posizioni uniche
            #     positions_list = sorted(
            #         context_data[context_data["Company"].isin(selected_companies)]["Position"].dropna().unique().tolist()
            #     )
            # else:
            #     # In assenza di selezione, carica tutte le posizioni
            positions_list = sorted(context_data["Position"].dropna().unique().tolist())

            # Multiselect per selezionare le posizioni (filtro aggiuntivo)
            selected_positions = st.multiselect("Filtro aggiuntivo: Seleziona le Posizioni", positions_list)

            # Tasto di ricerca unico
            if st.form_submit_button("Cerca"):
                # Filtra il DataFrame in base alle aziende e alle posizioni selezionate
                df_filtrato = company_advanced_search(context_data, selected_companies, selected_positions)
                if df_filtrato is not None:           
                    # Visualizza il DataFrame filtrato
                    st.dataframe(df_filtrato)
                    # 1️⃣ Livello Principale (Categorie - Aziende)
                    df = df_filtrato.groupby(["Position", "Company"]).size().reset_index(name="count")
                    if option == 'Company':
                        fig = px.bar(
                            df,
                            x="Position",
                            y="count",
                            title="Positions in Selected Companies",
                            color = "Company",
                            text_auto = True,
                            barmode="stack"
                        )

                                # Personalizzazione del layout
                        fig.update_layout(
                            xaxis_title="Position",
                            yaxis_title="count",
                            modebar_add=["resetScale2d"],
                            xaxis=dict(
                                rangeslider=dict(visible=True)),
                            template="plotly_white"  # Tema chiaro
                        )
                    else:
                        fig = px.bar(
                            df,
                            x="Company",
                            y="count",
                            title="Companies with selected Positions",
                            color = "Position",
                            text_auto = True,
                            barmode="stack"
                        )

                                # Personalizzazione del layout
                        fig.update_layout(
                            xaxis_title="Company",
                            yaxis_title="count",
                            modebar_add=["resetScale2d"],
                            xaxis=dict(rangeslider=dict(visible=True)),
                            template="plotly_white"  # Tema chiaro
                        )
                    # Mostra il grafico
                    st.plotly_chart(fig)
                else:
                    st.warning("Nessun dato trovato per i criteri selezionati.")
            else:
                st.warning("Seleziona almeno un'azienda per effettuare la ricerca.")
else:
    st.warning("Carica un file nella pagina Home per accedere a questa sezione.")