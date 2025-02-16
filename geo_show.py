import pandas as pd
import plotly.express as px

geo_df = pd.read_csv('geolocalizzazione_aziende.csv')
# Rimuovere eventuali valori nulli prima di visualizzare la mappa
geo_df_clean = geo_df.dropna(subset=["Latitudine", "Longitudine"])

# Creare la mappa con Plotly
fig = px.scatter_geo(
    geo_df_clean,
    lat="Latitudine",
    lon="Longitudine",
    color = "Company",
    size = "Count",
    title="Mappa Geografica dei Contatti Linkedin",
    projection="natural earth"
)

# Mostrare la mappa
fig.show()