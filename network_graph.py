import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import ast

# Caricamento del file CSV
file_path = "isp.csv"  # Assicurati che il file sia nella stessa cartella dello script
df = pd.read_csv(file_path)

# Creazione del grafo a più livelli
G = nx.DiGraph()

# Aggiunta dei nodi e degli archi con più livelli
for _, row in df.iterrows():
    entity_lei = row["LEI"]
    entity_name = row["Legal Name"]

    # Aggiunta del nodo principale
    G.add_node(entity_lei, label=entity_name, type="entity")

    # Collegamento con il parent diretto
    if pd.notna(row["Parent LEI"]):
        parent_lei = row["Parent LEI"]
        parent_name = row["Parent Name"]
        G.add_node(parent_lei, label=parent_name, type="direct_parent")
        G.add_edge(parent_lei, entity_lei, relationship="direct_parent")

    # Collegamento tra ultimate parent e direct parent
    if pd.notna(row["Ultimate Parent LEI"]) and pd.notna(row["Parent LEI"]):
        G.add_edge(row["Ultimate Parent LEI"], row["Parent LEI"], relationship="ultimate_to_direct")

    # Collegamento con l'ultimate parent
    if pd.notna(row["Ultimate Parent LEI"]):
        ultimate_parent_lei = row["Ultimate Parent LEI"]
        ultimate_parent_name = row["Ultimate Parent Name"]
        G.add_node(ultimate_parent_lei, label=ultimate_parent_name, type="ultimate_parent")
        G.add_edge(ultimate_parent_lei, entity_lei, relationship="ultimate_parent")

    # Aggiunta dei figli diretti
    if pd.notna(row["Direct Children"]):
        try:
            children_list = ast.literal_eval(row["Direct Children"])
            for child in children_list:
                child_lei = child["LEI"]
                child_name = child["Name"]
                G.add_node(child_lei, label=child_name, type="direct_child")
                G.add_edge(entity_lei, child_lei, relationship="direct_child")
        except:
            pass

    # Aggiunta degli ultimate children
    if pd.notna(row["Ultimate Children"]):
        try:
            ultimate_children_list = ast.literal_eval(row["Ultimate Children"])
            for child in ultimate_children_list:
                child_lei = child["LEI"]
                child_name = child["Name"]
                G.add_node(child_lei, label=child_name, type="ultimate_child")
                G.add_edge(entity_lei, child_lei, relationship="ultimate_child")

                # Collegamento tra direct children e ultimate children
                if child_lei in G.nodes:
                    G.add_edge(child_lei, entity_lei, relationship="ultimate_to_direct")
        except:
            pass

# Posizionamento dei nodi con più livelli
pos = nx.spring_layout(G, seed=42)

# Creazione delle liste per gli archi
edge_x, edge_y, edge_text = [], [], []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])
    edge_text.append(G.edges[edge].get("relationship", ""))

# Creazione delle liste per i nodi
node_x, node_y, node_text, node_colors = [], [], [], []
color_map = {
    "ultimate_parent": "blue",
    "direct_parent": "orange",
    "entity": "red",
    "direct_child": "purple",
    "ultimate_child": "cyan"
}

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(G.nodes[node]["label"])
    node_colors.append(color_map.get(G.nodes[node].get("type", "entity"), "gray"))

# Creazione del grafico interattivo con Plotly
fig = go.Figure()

# Aggiunta delle linee per gli archi
fig.add_trace(go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='black'),
    hoverinfo='text',
    mode='lines',
    text=edge_text
))

# Aggiunta dei nodi
fig.add_trace(go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    marker=dict(size=10, color=node_colors),
    text=node_text,
    textposition="top center",
    hoverinfo='text'
))

# Configurazione del layout
fig.update_layout(
    title="Network Graph (Multi-Level)",
    showlegend=False,
    hovermode='closest',
    margin=dict(b=20, l=5, r=5, t=40),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
)

# Mostra il grafo
fig.show()
