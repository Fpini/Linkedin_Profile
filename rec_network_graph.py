import requests
import networkx as nx
import plotly.graph_objects as go
import ast
import time

GLEIF_API_URL = "https://api.gleif.org/api/v1/lei-records/"

def get_lei_data(lei_code):
    """Ottiene i dati di un'azienda tramite codice LEI dall'API GLEIF."""
    response = requests.get(f"{GLEIF_API_URL}{lei_code}")

    if response.status_code != 200:
        return None

    return response.json()

def build_recursive_graph(G, lei_code, visited=set(), depth=3):
    """
    Costruisce ricorsivamente il grafo delle aziende collegate partendo da un codice LEI.
    
    Args:
        G (networkx.DiGraph): Grafo NetworkX da costruire.
        lei_code (str): Codice LEI di partenza.
        visited (set): Insieme di LEI già visitati per evitare cicli.
        depth (int): Profondità massima della ricerca (default: 3 livelli).
    """
    if lei_code in visited or depth == 0:
        return
    visited.add(lei_code)

    data = get_lei_data(lei_code)
    if not data:
        return

    attributes = data["data"]["attributes"]
    entity = attributes["entity"]
    registration = attributes["registration"]

    # Aggiunge nodo principale
    G.add_node(lei_code, label=entity["legalName"]["name"], type="company")

    relationships = data["data"].get("relationships", {})

    # Collega il Parent
    if "direct-parent" in relationships and "links" in relationships["direct-parent"]:
        parent_url = relationships["direct-parent"]["links"].get("lei-record")
        if parent_url:
            parent_data = get_lei_data(parent_url.split("/")[-1])
            if parent_data:
                parent_lei = parent_data["data"]["attributes"]["lei"]
                parent_name = parent_data["data"]["attributes"]["entity"]["legalName"]["name"]
                G.add_node(parent_lei, label=parent_name, type="parent")
                G.add_edge(parent_lei, lei_code, relationship="direct_parent")
                build_recursive_graph(G, parent_lei, visited, depth-1)

    # Collega l'Ultimate Parent
    if "ultimate-parent" in relationships and "links" in relationships["ultimate-parent"]:
        ultimate_parent_url = relationships["ultimate-parent"]["links"].get("lei-record")
        if ultimate_parent_url:
            ultimate_parent_data = get_lei_data(ultimate_parent_url.split("/")[-1])
            if ultimate_parent_data:
                ultimate_parent_lei = ultimate_parent_data["data"]["attributes"]["lei"]
                ultimate_parent_name = ultimate_parent_data["data"]["attributes"]["entity"]["legalName"]["name"]
                G.add_node(ultimate_parent_lei, label=ultimate_parent_name, type="ultimate_parent")
                G.add_edge(ultimate_parent_lei, lei_code, relationship="ultimate_parent")
                build_recursive_graph(G, ultimate_parent_lei, visited, depth-1)

    # Collega i Direct Children
    if "direct-children" in relationships and "links" in relationships["direct-children"]:
        children_url = relationships["direct-children"]["links"].get("related")
        if children_url:
            children_data = requests.get(children_url).json()
            if "data" in children_data:
                for child in children_data["data"]:
                    child_lei = child["attributes"]["lei"]
                    child_name = child["attributes"]["entity"]["legalName"]["name"]
                    G.add_node(child_lei, label=child_name, type="direct_child")
                    G.add_edge(lei_code, child_lei, relationship="direct_child")
                    build_recursive_graph(G, child_lei, visited, depth-1)

    # Collega gli Ultimate Children
    if "ultimate-children" in relationships and "links" in relationships["ultimate-children"]:
        ultimate_children_url = relationships["ultimate-children"]["links"].get("related")
        if ultimate_children_url:
            ultimate_children_data = requests.get(ultimate_children_url).json()
            if "data" in ultimate_children_data:
                for child in ultimate_children_data["data"]:
                    child_lei = child["attributes"]["lei"]
                    child_name = child["attributes"]["entity"]["legalName"]["name"]
                    G.add_node(child_lei, label=child_name, type="ultimate_child")
                    G.add_edge(lei_code, child_lei, relationship="ultimate_child")
                    build_recursive_graph(G, child_lei, visited, depth-1)

    time.sleep(0.5)  # Per evitare rate limits

def visualize_graph(G):
    """Visualizza il grafo con Plotly."""
    pos = nx.spring_layout(G, seed=42)

    edge_x, edge_y, edge_text = [], [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_text.append(G.edges[edge].get("relationship", ""))

    node_x, node_y, node_text = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(G.nodes[node]["label"])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='black'),
        hoverinfo='text',
        mode='lines',
        text=edge_text
    ))

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(size=10, color='blue'),
        text=node_text,
        textposition="top center",
        hoverinfo='text'
    ))

    fig.update_layout(
        title="Grafo delle Aziende Collegate (LEI Network)",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    fig.show()

# Esempio di utilizzo
if __name__ == "__main__":
    lei_code = "5493000HZTVUYLO1D793"  # Inserisci un LEI valido
    G = nx.DiGraph()
    build_recursive_graph(G, lei_code, depth=3)
    visualize_graph(G)
