import plotly.express as px
import pandas as pd

# Imposta il tuo access token Mapbox
px.set_mapbox_access_token("pk.eyJ1IjoiZnBpbmkiLCJhIjoiY203N2ZzN3A5MDQ3czJqc2h2aHVmemU4bCJ9.Y51CADcs8wC70kIxfpI9XgOKEN")

# Creazione di un DataFrame con dati di esempio
df = pd.read_csv("geolocalizzazione_aziende.csv")
# Rimuovere eventuali valori nulli prima di visualizzare la mappa
df_clean = df.dropna(subset=["Latitudine", "Longitudine"])

# Creare la mappa con Mapbox
fig = px.scatter_mapbox(
    df_clean, 
    lat="Latitudine", 
    lon="Longitudine", 
    color="Company",  # Colore diverso per ogni azienda
    size = "Count",
    zoom=5,  # Livello di zoom
    mapbox_style="carto-darkmatter"  # Stile della mappa
)

# Mostrare la mappa
fig.show()
