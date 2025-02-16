import streamlit as st
import duckdb
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
import streamlit.components.v1 as components

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Elimina tutte le righe che hanno almeno un valore nullo
    df_clean = df.dropna(axis=0)
    # 2. Elimina le righe in cui, per almeno una colonna di tipo stringa,
    #    la lunghezza del contenuto trimmato è inferiore alla lunghezza originale
    def row_has_extra_spaces(row):
        for val in row:
            if isinstance(val, str):
                # Se la lunghezza della stringa senza spazi iniziali/finali è minore,
                # significa che c'erano spazi extra
                if len(val.strip()) < len(val):
                    return True
        return False

    # Applica la funzione su ogni riga e conserva quelle che non hanno spazi extra
    mask = ~df_clean.apply(row_has_extra_spaces, axis=1)
    df_clean = df_clean[mask]
    
    return df_clean

def upload_file():
    return st.sidebar.file_uploader("Carica un file (CSV)", type=["csv"])


def get_duckdb_connection():
    if "duckdb_conn" not in st.session_state:
        st.session_state["duckdb_conn"] = duckdb.connect(database=":memory:", read_only=False)
    return st.session_state["duckdb_conn"]

@st.cache_data
def process_csv_file(file):
    try:
        filename = file.name
        conn = get_duckdb_connection()
        a = conn.execute (f'''CREATE TABLE Connections AS SELECT * FROM read_csv('{filename}')''')
        context_data = conn.sql('''select * from Connections''').df()
        #context_data = clean_dataframe(context_data)
        if context_data.empty:
            st.error("Il file caricato è vuoto.")
            return None
        return context_data
    except Exception as e:
        st.error(f"Errore durante la lettura del file: {e}")
        return None
    
@st.cache_data
def company_count(context_data):
    try:
        conn = get_duckdb_connection()
        cnt = conn.sql('''SELECT COUNT(DISTINCT Company) from context_data''').fetchone()[0]
    except Exception as e:
        print(f"Errore catturato: {e}")
        cnt = 0  # O un valore di fallback  
    return cnt

@st.cache_data
def position_count(context_data):
    try:
        conn = get_duckdb_connection()
        cnt = conn.sql('''SELECT COUNT(DISTINCT Position) from context_data''').fetchone()[0]
    except Exception as e:
        print(f"Errore catturato: {e}")
        cnt = 0  # O un valore di fallback  
    return cnt

@st.cache_data
def connections_per_company(context_data):
    try:
        conn = get_duckdb_connection()
        df = conn.sql(f'''SELECT Company, count(*) as count_company from Connections group by all having count_company > 2 order by count_company desc ''').df()
    except Exception as e:
        print(f"Errore catturato: {e}")
        df = None  # O un valore di fallback  
    return df

@st.cache_data
def connections_per_position(context_data):
    try:
        conn = get_duckdb_connection()
        df = conn.sql(f'''SELECT Position, count(*) as count_position from context_data group by all having count_position > 2 order by count_position desc''').df()
    except Exception as e:
        print(f"Errore catturato: {e}")
        df = None  # O un valore di fallback  
    return df

@st.cache_data
def connections_progression(context_data):
    try:
        conn = get_duckdb_connection()
        sql_str = '''SELECT 
                        YEAR(STRPTIME("Connected On", '%d %b %Y')) AS year, 
                        MONTH(STRPTIME("Connected On", '%d %b %Y')) AS month, 
                        COUNT(*) AS monthly_count,
                        SUM(COUNT(*)) OVER (
                            PARTITION BY YEAR(STRPTIME("Connected On", '%d %b %Y')) 
                            ORDER BY MONTH(STRPTIME("Connected On", '%d %b %Y')) 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        ) AS cumulative_count
                    FROM Connections
                    GROUP BY year, month
                    ORDER BY year, month'''
        df = conn.sql(sql_str).df()
    except Exception as e:
        print(f"Errore catturato: {e}")
        df = None  # O un valore di fallback  
    return df

@st.cache_data
def connections_progression_global(context_data):
    try:
        conn = get_duckdb_connection()
        sql_str = '''SELECT 
                        YEAR(STRPTIME("Connected On", '%d %b %Y')) AS year, 
                        MONTH(STRPTIME("Connected On", '%d %b %Y')) AS month, 
                        COUNT(*) AS monthly_count,
                        SUM(COUNT(*)) OVER (
                            ORDER BY YEAR(STRPTIME("Connected On", '%d %b %Y')), 
                                    MONTH(STRPTIME("Connected On", '%d %b %Y')) 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        ) AS cumulative_count
                    FROM context_data
                    GROUP BY year, month
                    ORDER BY year, month;
                '''
        df = conn.sql(sql_str).df()
    except Exception as e:
        print(f"Errore catturato: {e}")
        df = None  # O un valore di fallback
    return df 

@st.cache_data
def max_conn_prog_glb(conn_prog_glb):
    try:
        conn = get_duckdb_connection()
        sql_str= '''SELECT MAX(cumulative_count) FROM conn_prog_glb'''
        n = int(conn.sql(sql_str).fetchone()[0])
    except Exception as e:
        print(f"Errore catturato: {e}")
        n = 0  # O un valore di fallback
    return n

@st.cache_data
def create_comp_subset(context_data, n):
    try:
        conn = get_duckdb_connection()
        sql_str= f'''SELECT Company, count(*) as compcount FROM context_data where NOT Company is NULL group by Company order by compcount desc LIMIT {n}'''
        df = conn.sql(sql_str).df()
        sql_str =  f'''SELECT AVG(compcount) as average, STDDEV(compcount) as deviation FROM df'''
        df_metriche = conn.sql(sql_str).df()
        df['diff'] = df['compcount'] - df_metriche['average'][0]
        df['compcountnorm'] = ((df['diff'] / df_metriche['deviation'][0]).round(0))
        df['compcountnorm'] = df['compcountnorm'] * 5
        df['compcountnorm'] = df['compcountnorm'].astype(int)
    except Exception as e:
        print(f"Errore catturato: {e}")
        df = None  # O un valore di fallback
    return df


def visualizza_grafo(context_data):
        G = crea_grafo(context_data)

#        pos = nx.fruchterman_reingold_layout(G, scale=2, iterations=30)  
#        pos = nx.spectral_layout(G)
        top_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:150]  # I 150 nodi con più connessioni
        subgraph = G.subgraph(dict(top_nodes).keys()).copy()
        pos = nx.spring_layout(subgraph)
#        pos = nx.fruchterman_reingold_layout(subgraph, scale=2, iterations=30)
#        pos = nx.spectral_layout(subgraph)  
        # Estrai le coordinate dei nodi
        node_x = []
        node_y = []
        node_sizes = []

        # for node, attributes in subgraph.nodes(data=True):
        #     st.write(f"Nodo {node}: {attributes}")

        for node in subgraph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_sizes.append(subgraph.nodes[node]['weight'] * 2)

        # Estrai le coordinate degli archi
        edge_x = []
        edge_y = []
        for edge in subgraph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)  # Serve per spezzare le linee tra i segmenti
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)     

        # Crea il trace degli archi
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='black'),
            hoverinfo='none',
            mode='lines'
        )       

        # Crea il trace dei nodi
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=[str(node) for node in G.nodes()],
            textposition="top center",
            hoverinfo='text',
            marker=dict(
                size=node_sizes,
                color='blue',
                line=dict(width=2, color='black')
            )
        )

        # Creazione della figura con Plotly
        # Creazione della figura con un pulsante di reset
        fig = go.Figure(data=[edge_trace, node_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                margin=dict(b=0, l=0, r=0, t=0),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                updatemenus=[  # Aggiunta di un pulsante di reset
                    dict(
                        type="buttons",
                        showactive=False,
                        buttons=[
                            dict(label="Reset Zoom",
                                method="relayout",
                                args=[{"xaxis.autorange": True, "yaxis.autorange": True}]
                            )
                        ],
                        x=0.1,  # Posizione orizzontale
                        y=1.1   # Posizione verticale
                    )
                ]
            )
        )
        # Mostra il grafico
#        fig.show()
        st.plotly_chart(fig, use_container_width=True)


def crea_grafo(context_data):
    # Creazione di un grafo diretto
    G = nx.DiGraph()

    # Aggiunta dei nodi al grafo con criptazione opzionale
    # soggetti['NOME_TRONCATO'] = soggetti.apply(
    #     lambda row: cripta(nominativo(row))[:10] if cripta_dati else nominativo(row)[:10], axis=1
    # )
    G.add_node('Me')
    G.nodes['Me']['weight'] = 5

    for _, row_ord in context_data.iterrows():
        company = row_ord['Company']
        if company is not None:
            if company not in G.nodes:
                G.add_node(company)
                G.add_edge('Me', company)
                G.nodes[company]['weight'] = row_ord['compcountnorm']
    return G

@st.cache_data
def company_connections_progression(context_data, user_input):
    try:
        like_cond = f"'%{user_input.upper()}%'"

        conn = get_duckdb_connection()
        sql_str = f'''SELECT 
                        UPPER(Company) as COMPANY,
                        YEAR(STRPTIME("Connected On", '%d %b %Y')) AS year, 
                        MONTH(STRPTIME("Connected On", '%d %b %Y')) AS month, 
                        COUNT(*) AS monthly_count,
                        SUM(COUNT(*)) OVER (
                            ORDER BY YEAR(STRPTIME("Connected On", '%d %b %Y')), 
                                    MONTH(STRPTIME("Connected On", '%d %b %Y')) 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        ) AS cumulative_count
                    FROM context_data
                    where UPPER(Company) like {like_cond}
                    GROUP BY Company, year, month
                    ORDER BY year, month, Company;
                '''

        df = conn.sql(sql_str).df()
        df["year_month"] = df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)
    except Exception as e:
        print(f"Errore catturato: {e}")
        df = None  # O un valore di fallback
    return df

@st.cache_data
def connections_per_company(context_data):
    try:
        conn = get_duckdb_connection()
        sql_str = f'''SELECT 
                        UPPER(Company) as company,
                        count(*) as con_per_comp
                    FROM context_data
                    GROUP BY UPPER(Company)
                    ORDER BY con_per_comp desc;
                '''
        df = conn.sql(sql_str).df()
    except Exception as e:
        print(f"Errore catturato: {e}")
        df = None  # O un valore di fallback
    return df

@st.cache_data
def positions_per_company(context_data):
    try:
        conn = get_duckdb_connection()
        sql_str = '''
            SELECT
                Company AS company,
                Position as position,
                COUNT(*) AS pos_per_comp
            FROM context_data
            where Company is not NULL and len(Company) > 1
            GROUP BY Company, Position
            HAVING pos_per_comp > 1
            order by pos_per_comp desc
        '''
        df = conn.sql(sql_str).df()
        df["company"] = df["company"].fillna("Unknown")
        df["position"] = df["position"].fillna("Unknown")
        #df["url"] = df["url"].fillna("Unknown")
        #df = df[df["company"] > "."]
        # Debugging: Mostra le colonne disponibili
        st.write("Colonne disponibili nel DataFrame:", df.columns)


        return df  # Ritorna il DataFrame per debugging
    except Exception as e:
        st.error(f"Errore catturato: {e}")
        return None  # Fallback in caso di errore

@st.cache_data
def create_df_per_map(context_data):
    # Rimuovere eventuali valori nulli prima di visualizzare la mappa
    geo_df_clean = context_data.dropna(subset=["Latitude", "Longitude"])

    geo_df_grouped = geo_df_clean.groupby(["Company", "Latitude","Longitude"]).size().reset_index(name="Count")

    return geo_df_grouped

@st.cache_data
def create_df_per_map2(context_data):
    # Rimuovere eventuali valori nulli prima di visualizzare la mappa
    geo_df_clean = context_data.dropna(subset=["Latitude", "Longitude"])

    geo_df_grouped = geo_df_clean.groupby(["Company", "Location", "Latitude","Longitude"]).size().reset_index(name="Count")

    st.write(geo_df_grouped)

    return geo_df_grouped