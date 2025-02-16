import pandas as pd
import plotly.express as px

geo_df = pd.read_csv('geo_Connections.csv')
# Rimuovere eventuali valori nulli prima di visualizzare la mappa
geo_df_clean = geo_df.dropna(subset=["Latitude", "Longitude"])

df_grouped = geo_df_clean.groupby(["Company", "Latitude","Longitude"]).size().reset_index(name="Count")
# Creare la mappa con Plotly
fig = px.scatter_geo(
    df_grouped,
    lat="Latitude",
    lon="Longitude",
    color = "Company",
    size = "Count",
    title="Linkedin Connection Map",
    projection="natural earth"
)

# Mostrare la mappa
fig.show()