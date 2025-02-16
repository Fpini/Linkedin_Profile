import pandas as pd
import plotly.express as px

geo_df = pd.read_csv('geo_Connections.csv')
# Rimuovere eventuali valori nulli prima di visualizzare la mappa
geo_df_clean = geo_df.dropna(subset=["Latitude", "Longitude"])

df = geo_df_clean.groupby(["Company", "Location", "Latitude","Longitude"]).size().reset_index(name="Count")

# Imposta il tuo access token Mapbox
px.set_mapbox_access_token("pk.eyJ1IjoiZnBpbmkiLCJhIjoiY203N2ZzN3A5MDQ3czJqc2h2aHVmemU4bCJ9.Y51CADcs8wC70kIxfpI9XgOKEN")

# Creare la mappa con Mapbox
fig = px.scatter_mapbox(
    df, 
    lat="Latitude", 
    lon="Longitude", 
    color="Company",  # Colore diverso per ogni azienda
    size = "Count",
    zoom=3,  # Livello di zoom
    mapbox_style="carto-positron",
    hover_name="Company",
    hover_data=["Count", "Location", "Latitude","Longitude"]  # Stile della mappa
)

fig.update_layout(dragmode="pan", showlegend=False, uirevision="static")

# fig.update_layout(mapbox_center={"lat": df["Latitude"].mean(), "lon": df["Longitude"].mean()},  # Centro della mappa
#                                  dragmode="pan", showlegend=False, uirevision="static")

# Mostrare la mappa
fig.show()

